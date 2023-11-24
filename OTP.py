#https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client

# Set environment variables for your credentials
# http://twil.io/secure


account_sid = "AC24c3fb534d313b273e3b8ae9ea979e71"
auth_token = "885eaa15ede70859f9f49c2c241e853b"
verify_sid = "VAbb60d6d76f85f7124c36bcf6e11a56d3"
contact = None

client = Client(account_sid, auth_token)
def send_OTP(contact):
    verification = client.verify.v2.services(verify_sid) \
    .verifications \
    .create(to=contact, channel="sms")
    return verification.status


def checks_OTP(contact, otp_code):
    verification_check = client.verify.v2.services(verify_sid) \
    .verification_checks \
    .create(to=contact, code=otp_code)
    return verification_check.status
