from django.shortcuts import render, redirect
import requests
import json

# Create your views here.
def home(request):
    return render(request, "index.html")


def devs(request):
    return render(request, "devs.html")


def init(request):
    if request.method == "POST":
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        height = float(request.POST.get("height"))
        weight = float(request.POST.get("weight"))
        bmi = weight / ((height * 0.01) ** 2)
        print(age, sex, bmi)
        request.session["age"] = age
        request.session["sex"] = sex
        request.session["bmi"] = bmi
        return redirect(choose_track)
    return render(request, "init.html")


def choose_track(request):
    return render(request, "cards.html")


def search(request):
    age = int(request.session.get("age"))
    url = f"https://api.infermedica.com/v3/symptoms?age.value={age}"
    payload = {}
    headers = {"App-Id": "b1e005c3", "App-Key": "2301a8a155cbd654683d517727c36990"}
    response = requests.request("GET", url, headers=headers, data=payload)
    symptoms = response.json()
    return render(request, "search.html", {"symptoms": symptoms})


def complaint(request):
    return render(request, "complaint.html")


def labresult(request):
    url = f"https://api.infermedica.com/v3/concepts?types=lab_test"
    payload = {}
    headers = {"App-Id": "b1e005c3", "App-Key": "2301a8a155cbd654683d517727c36990"}
    response = requests.request("GET", url, headers=headers, data=payload)
    symptoms = response.json()
    return render(request, "labresults.html", {"symptoms": symptoms})


def init_evidence(request):
    age = request.session.get("age")
    track = request.session.get("track")
    context = {
        "age": age,
        "sex": request.session.get("sex"),
        "track": track,
    }
    if track == "text":
        return render(request, "init_evidence.html", context)
    if track == "search":
        url = f"https://api.infermedica.com/v3/symptoms?age.value={age}"
    else:
        url = f"https://api.infermedica.com/v3/concepts?types=lab_test"
    payload = {}
    headers = {"App-Id": "b1e005c3", "App-Key": "2301a8a155cbd654683d517727c36990"}
    response = requests.request("GET", url, headers=headers, data=payload)
    symptoms = response.json()
    context.update({"symptoms": symptoms})
    return render(request, "init_evidence.html", context)


def risk_factors(request):
    age = int(request.session.get("age"))
    sex = request.session.get("sex")
    bmi = request.session.get("bmi")
    user_data = {"sex": sex, "age": {"value": age}, "extras": {"disable_groups": True}}
    evidence = []
    if bmi > 30:
        evidence.append({"id": "p_7", "choice_id": "present", "source": "predefined"})
    elif bmi < 19:
        evidence.append({"id": "p_6", "choice_id": "present", "source": "predefined"})
    if "sub-1" in request.POST:
        complaint = request.POST.get("complaint")
        url = "https://api.infermedica.com/v3/parse"

        payload = json.dumps({"age": {"value": age}, "sex": sex, "text": complaint})
        headers = {
            "App-Id": "b1e005c3",
            "App-Key": "2301a8a155cbd654683d517727c36990",
            "Content-Type": "application/json",
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        symptoms = response.json()["mentions"]
        for i in symptoms:
            evidence.append(
                {"id": i["id"], "choice_id": "present", "source": "initial"}
            )
        user_data.update({"evidence": evidence})
        request.session["user_data"] = user_data
    elif "sub-2" in request.POST:
        data = request.POST.getlist("sel[]")
        for i in data:
            evidence.append({"id": i, "choice_id": "present", "source": "initial"})
        user_data.update({"evidence": evidence})
        request.session["user_data"] = user_data

    url = "https://api.infermedica.com/v3/suggest"
    payload = json.dumps(
        {
            "sex": sex,
            "age": {"value": age},
            "suggest_method": "risk_factors",
            "evidence": evidence,
        }
    )
    headers = {
        "App-Id": "b1e005c3",
        "App-Key": "2301a8a155cbd654683d517727c36990",
        "Content-Type": "application/json",
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    factors = response.json()
    return render(request, "select_factors.html", {"factors": factors})


def questions(request):
    user_data = request.session.get("user_data")
    evidence = user_data["evidence"]
    url = "https://api.infermedica.com/v3/diagnosis"
    headers = {
        "App-Id": "b1e005c3",
        "App-Key": "2301a8a155cbd654683d517727c36990",
        "Content-Type": "application/json",
    }
    if "factors" in request.POST:
        print("got risk factors")
        data = request.POST.getlist("sel[]")
        for i in data:
            evidence.append({"id": i, "choice_id": "present", "source": "suggest"})
        user_data["evidence"] = evidence
        request.session["user_data"] = user_data

    if "choice" in request.POST:
        print("got answer")
        temp = request.POST.get("answer")
        symptom = temp.split(",")[0]
        choice = temp.split(",")[1]
        user_data["evidence"].append({"id": symptom, "choice_id": choice})
        request.session["user_data"] = user_data
        payload = json.dumps(user_data)
        response = requests.request("POST", url, headers=headers, data=payload)
        response.json()["should_stop"]
        if response.json()["should_stop"]:
            conditions = response.json()["conditions"]
            request.session["conditions"] = conditions
            return redirect(diagnosis)
        else:
            question = response.json()["question"]
            return render(request, "questions.html", {"question": question})

    payload = json.dumps(user_data)
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.json()["should_stop"]:
        return redirect(diagnosis)
    # print(response.json())
    question = response.json()["question"]
    return render(request, "questions.html", {"question": question})


def diagnosis(request):
    conditions = request.session.get("conditions")
    return render(request, "diagnosis.html", {"conditions": conditions})
