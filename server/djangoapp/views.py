from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import CarMake, CarModel
from .populate import initiate
from .restapis import get_request, analyze_review_sentiments, post_review
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
        return JsonResponse(
            {"error": "Username and password are required"}, status=400
        )

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
        return JsonResponse(
            {"userName": username, "error": "Already Registered"}
        )

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
        email=email,
    )
    login(request, user)
    return JsonResponse({"userName": username, "status": "Authenticated"})


def get_dealerships(request, state="All"):
    endpoint = "/fetchDealers" if state == "All" else "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    dealership = get_request("/fetchDealer/" + str(dealer_id))
    return JsonResponse({"status": 200, "dealer": [dealership]})


def get_dealer_reviews(request, dealer_id):
    if not dealer_id:
        return JsonResponse({"status": 400, "message": "Bad Request"})

    reviews = get_request("/fetchReviews/dealer/" + str(dealer_id))
    for review_detail in reviews:
        sentiment = analyze_review_sentiments(review_detail["review"])
        review_detail["sentiment"] = (
            sentiment.get("sentiment", "neutral") if sentiment else "neutral"
        )

    return JsonResponse({"status": 200, "reviews": reviews})


@csrf_exempt
def add_review(request):
    if request.user.is_anonymous:
        return JsonResponse({"status": 403, "message": "Unauthorized"})

    try:
        data = json.loads(request.body)
        response = post_review(data)
        if response is None:
            return JsonResponse(
                {"status": 401, "message": "Error in posting review"}
            )
        return JsonResponse({"status": 200})
    except Exception:
        return JsonResponse(
            {"status": 401, "message": "Error in posting review"}
        )


def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)

    if count == 0:
        initiate()

    car_models = CarModel.objects.select_related("car_make")
    cars = []

    for car_model in car_models:
        cars.append(
            {"CarModel": car_model.name, "CarMake": car_model.car_make.name}
        )

    return JsonResponse({"CarModels": cars})
