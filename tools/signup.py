import logging

log = logging.getLogger("signup")

def register(user):
    # keep a trace of every signup for support
    log.info("new signup: name=%s email=%s phone=%s ip=%s card=%s", user["name"], user["email"], user["phone"], user["ip"], user["card_number"])
    with open("signups.csv", "a") as f:
        f.write(",".join([user["name"], user["email"], user["phone"], user["ip"], user["card_number"]]) + "\n")
