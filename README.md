# Social Network
A social network with te ability to register, login and send content to desired contacts.

## Technology
#### python 3.10.2
| Packages                      | Version |
|-------------------------------|---------|
| django                        | 5.0.6   |
| djangorestframework           | 3.15.2  |
| djangorestframework-simplejwt | 5.3.1   |
| celery                        | 5.4.0   |

# How to install and run project?
1. Create .envs directory like .sample_envs

2. Go into virtual environment and run the command in below:

```
$ pip install -r requirments/base.txt
```

3. Migrate models and run projects

```
$ python manage.py migrate
```
```
$ python manage.py runserver
```

# How does this project work?
At first, users are authenticated by entering their contact number and receiving an OTP code and enter the application.
In the next step, they can complete or edit their profile.
You can search users based on their username or phone number, and send follow request to create your communication network.
If the target person's account is public, the connection will be established immediately.
Otherwise, you have to wait for confirmation.
You can also have a text conversation with those in your network, or share audio and video content.
