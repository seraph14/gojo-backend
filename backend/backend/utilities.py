from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification


def notify_new_unseen_chat(my_registration_token, sender, message):
    pass

# data = FCMDevice.objects.send_message(
#     Message(notification=Notification(title="From Django", body="testing" , image="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQM7nz32LAtaF2uwCeyNNFdPZU9ySxpuZOljo4H_3t_&s")), additional_registration_ids=["ef3KyiNgTUqeQNi6w_NTkq:APA91bE6FVFHGBfmn98lGIgtnL_Nfct_YV2nu79fjzo5KveJOc-ynbCQS86R7DfnASVWQ2w7OZWj1PCDoCdWg8OQBmcSytPYDmfwpjzTlyMc9I_DUE-2iPwW1FvjtGYNSXhuhJxpy8x9"]
# )

# print(data.response.failure_count)
# data.response.responses[0]

# data.response._responses
# FCMDevice.objects.create(registration_id="ef3KyiNgTUqeQNi6w_NTkq:APA91bE6FVFHGBfmn98lGIgtnL_Nfct_YV2nu79fjzo5KveJOc-ynbCQS86R7DfnASVWQ2w7OZWj1PCDoCdWg8OQBmcSytPYDmfwpjzTlyMc9I_DUE-2iPwW1FvjtGYNSXhuhJxpy8x9", type="android")
# +