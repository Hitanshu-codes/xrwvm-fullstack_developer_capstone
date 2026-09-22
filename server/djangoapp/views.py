from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import CarMake, CarModel
from .populate import initiate
import logging
import json
from django.views.decorators.csrf import csrf_exempt


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data["userName"]
        password = data["password"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return JsonResponse({"error": "Username and password are required"}, status=400)

    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_user(request):
    username = request.user.username if request.user.is_authenticated else ""
    logout(request)
    return JsonResponse({"userName": "" if username else ""})


@csrf_exempt
def registration(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required"}, status=405)

    try:
        data = json.loads(request.body)
        username = data["userName"].strip()
        password = data["password"]
        first_name = data.get("firstName", "").strip()
        last_name = data.get("lastName", "").strip()
        email = data.get("email", "").strip()
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
        return JsonResponse(
            {"error": "All registration fields are required"}, status=400
        )

    if not username or not password or not email:
        return JsonResponse(
            {"error": "All registration fields are required"}, status=400
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse({"userName": username, "error": "Already Registered"})

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


# # Update the `get_dealerships` view to render the index page with
# a list of dealerships
# def get_dealerships(request):
# ...

# Create a `get_dealer_reviews` view to render the reviews of a dealer
# def get_dealer_reviews(request,dealer_id):
# ...

# Create a `get_dealer_details` view to render the dealer details
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request):
# ...


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []

    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})

    return JsonResponse({"CarModels": cars})
