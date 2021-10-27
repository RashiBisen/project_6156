import json

secure_paths = [
    "/users"
]


def check_auth(request, google, blueprint):

    path = request.path
    result_ok = False
    if path in secure_paths:
        google_data = None

        user_info_endpoint = '/oauth2/v2/userinfo'

        if google.authorized:
            google_data = google.get(user_info_endpoint).json()

            #print(json.dumps(google_data, indent=2))
            domain = google_data["email"].split("@")[-1]
            if domain != "columbia.edu":
                print("Use your Lion mail for logging in!!")
                result_ok = False
                return result_ok
            s = blueprint.session
            t = s.token
            print("Token = \n", json.dumps(t, indent=2))

            result_ok = True
    else:
        result_ok = True

    return result_ok
