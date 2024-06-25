from drf_yasg import openapi

CommonOkOutputString = "OK"
ListTypePathParamRegex = "(?P<type>[^/.]+)"

manualParametersDictCons = dict(
    default=openapi.Parameter(
        "source",
        in_=openapi.IN_HEADER,
        type=openapi.TYPE_STRING,
        default="app",
        required=True,
        enum=["app", "pwa"],
    ),
)
