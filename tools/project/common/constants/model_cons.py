from django.db.models import TextChoices


class UserRoleChoice(TextChoices):
    CUSTOMER = "customer", "مشتری"
    ADMIN = "admin", "مدیر سامانه"
    SCHOOL_HEAD_MASTER = "school_head_master", "مدرسه"
    APPS = "apps", "اپ"


class AppName(TextChoices):
    STUDENT_INSURANCE = "student_insurance", "حوادث دانش آموزی"
    IRANIAN_CUSTOMER = "IRANIAN_customer", "اپ مشتری ایرانیان پوشش"
    ASI_CUSTOMER = "ASI_customer", "اپ مشتری آسیا"
    ASI_AGENT = "ASI_agent", "اپ نماینده آسیا"
    DEY_CUSTOMER = "DEY_customer", "اپ مشتری دی"
    DEY_AGENT = "DEY_agent", "اپ نماینده دی"
    ADJUSTER_VEHICLE_APP = "Adjuster_vehicle_app", "اپ کارشناس اتومبیل"
    IRA_CUSTOMER = "IRA_customer", "اپ مشتری ایران"
    IRA_AGENT = "IRA_agent", "اپ نماینده ایران"
    HAF_AGENT = "HAF_agent", "اپ نماینده حافظ"
    HAF_CUSTOMER = "HAF_customer", "اپ مشتری حافظ"
    DAN_AGENT = "DAN_agent", "اپ نماینده دانا"
    DAN_CUSTOMER = "DAN_customer", "اپ مشتری دانا"
    REF_CUSTOMER = "REF_customer", "اپ مشتری رفاپ"
    PAR_AGENT = "PAR_agent", "اپ نماینده پارسیان"
    PAR_CUSTOMER = "PAR_customer", "اپ مشتری پارسیان"
    TEJ_AGENT = "TEJ_agent", "اپ نماینده تجارت نو"
    TEJ_CUSTOMER = "TEJ_customer", "اپ مشتری تجارت نو"
    ALB_AGENT = "ALB_agent", "اپ نماینده البرز"
    ALB_CUSTOMER = "ALB_customer", "اپ مشتری البرز"
    KAR_AGENT = "KAR_agent", "اپ نماینده کارآفرین"
    KAR_CUSTOMER = "KAR_customer", "اپ مشتری کارآفرین"
    ASM_AGENT = "ASM_agent", "اپ نماینده آسماری"
    ASM_CUSTOMER = "ASM_customer", "اپ مشتری آسماری"
    SIN_AGENT = "SIN_agent", "اپ نماینده سینا"
    SIN_CUSTOMER = "SIN_customer", "اپ مشتری سینا"
    SAR_AGENT = "SAR_agent", "اپ نماینده سرمد"
    SAR_CUSTOMER = "SAR_customer", "اپ مشتری سرمد"
    RAZ_AGENT = "RAZ_agent", "اپ نماینده رازی"
    RAZ_CUSTOMER = "RAZ_customer", "اپ مشتری رازی"
    AUTOMOBILE_PORTAL = "automobile_portal", "پورتال انومبیل"
    ESTATE_PORTAL = "estate_portal", "پورتال اموال"
    ESTATE_ADJUSTER = "estate_adjuster", "اپ کارشناس اموال"


class InsuranceCodeChoice(TextChoices):
    ASI = "ASI", "آسیا"
    IRA = "IRA", "ایران"
    ALB = "ALB", "البرز"
    DAN = "DAN", "دانا"
    PAR = "PAR", "پارسیان"
    PAS = "PAS", "پاسارگاد"
    RAZ = "RAZ", "رازی"
    MEL = "MEL", "ملت"
    MA = "MA", "ما"
    KAR = "KAR", "کارآفرین"
    DEY = "DEY", "دی"
    SAM = "SAM", "سامان"
    SIN = "SIN", "سینا"
    NOV = "NOV", "نوین"
    MOA = "MOA", "معلم"
    MIH = "MIH", "میهن"
    KOW = "KOW", "کوثر"
    ARM = "ARM", "آرمان"
    TAA = "TAA", "تعاون"
    TEJ = "TEJ", "تجارت نو"
    SAR = "SAR", "سرمد"
    HEK = "HEK", "حکمت صبا"
    ASM = "ASM", "آسماری"
    OMI = "OMI", "امید"
    TOS = "TOS", "توسعه"
    KHA = "KHA", "زندگی خاورمیانه"
    HAF = "HAF", "حافظ"
    MOE = "MOE", "معین"
    AMI = "AMI", "اتکایی امین"
    BAR = "BAR", "برکت"
    YAR = "YAR", "یاری رسان تارا پارس"
    BAZ = "BAZ", "بازار"
    KIS = "KIS", "متقابل كيش"
    EIR = "EIR", "اتکایی ایرانیان"
    GHE = "GHE", "متقابل اطمينان متحد قشم"
    PAD = "PAD", "پردیس"
    CHZ = "CHZ", "کاریزما"


class SchoolTypeNameChoice(TextChoices):
    NORMAL_STATE = "state", "عادی دولتی"
    GOVERNMENT_SAMPLE = "government_sample", "نمونه دولتی"
    NON_PROFIT = "non_profit", "غیر دولتی"
    BRILLIANT_TALENTS = "brilliant_talents", "استعدادهای درخشان"
    SHAHED = "shahed", "شاهد"
    SACRIFICERS = "sacrificers", "ایثارگران"
    BOARDING = "boarding", "شبانه روزی"
    ADULTS = "adults", "بزرگسالان"
    NOMADIC = "nomadic", "عشایری"
    FIRST_DEPENDENT = "first_dependent", "وابسته نوع اول"
    SECOND_DEPENDENT = "second_dependent", "وابسته نوع دوم"
    INTERNATIONAL = "international", "بین المللی"
    NON_GOVERNMENTAL_SUPPORT = "non_governmental_support", "غیر دولتی حمایتی"
    LONG_DISTANCE_NON_PROFIT = "long_distance_non_profit", "آموزش از راه دور غیر دولتی"
    BOARD_TRUSTEES = "board_trustees", "هیئت امنائی"
    QURAN_SCHOOL = "quran_school", "مدرسه قرآن"
    SPORT_SCHOOL = "sport_school", "مجتمع ورزشی"
    CHARITY_NON_PROFIT = "charity_non_profit", "غیر دولتی خیریه"
    DAR_AL_QURAN = "dar_al_quran", "دارالقرآن"
    LD = "LD", "مرکز L.D"
    OTHER = "other", "سایر"


class PurchaseMethodNameChoice(TextChoices):
    CONFIRM_BEFORE_PAYMENT = "confirm_before_payment", "نیازمند تایید مدرسه پیش از پرداخت"
    NO_CONFIRM = "no_confirm", "عدم نیاز به تایید مدرسه"
    CONFIRM_AFTER_PAYMENT = "confirm_after_payment", "نیازمند تایید پس از پرداخت"


class CreatorUserTypeChoice(TextChoices):
    STUDENT = "student", "دانش آموز"
    EMPLOYEE = "employee", "کارمند"
    ADMIN = "admin", "مدیر سامانه"


class PanelCreatorUserTypeChoice(TextChoices):
    EMPLOYEE = "employee", "کارمند"
    ADMIN = "admin", "مدیر سامانه"


class CreatorOrderUserTypeChoice(TextChoices):
    STUDENT = "student", "دانش آموز"
    EMPLOYEE = "employee", "کارمند"


class FileTypeChoice(TextChoices):
    STUDENT_INCIDENTS = "student_incidents", "حوادث دانش آموزی"


class GenderChoice(TextChoices):
    MALE = "male", "مرد"
    FEMALE = "female", "زن"


class NationalityChoice(TextChoices):
    IRANIAN = "iranian", "ایرانی"
    NON_IRANIAN = "non_iranian", "غیر ایرانی"


class EducationTypeNameChoice(TextChoices):
    EXCEPTIONAL_KINDERGARTEN = "exceptional_kindergarten", "کودکستان استثنايی"
    PRESCHOOL = "preschool", "پیش دبستانی"
    DESCRIPTIVE_ELEMENTARY_SCHOOL = "descriptive_elementary_school", "ابتدایی توصیفی"
    EXCEPTIONAL_ELEMENTARY_SCHOOL = "exceptional_elementary_school", "ابتدایی استثنائی"
    FIRST_HIGH_SCHOOL = "first_high_school", "متوسطه اول"
    LONG_DISTANCE_FIRST_HIGH_SCHOOL = "long_distance_first_high_school", "متوسطه اول راه دور"
    EXCEPTIONAL_FIRST_HIGH_SCHOOL = "exceptional_first_high_school", "متوسطه اول استثنائی"
    EXCEPTIONAL_PRE_PROFESSIONAL_FIRST_HIGH_SCHOOL = (
        "exceptional_pre_professional_first_high_school",
        "متوسطه اول پیش حرفه ای استثنائی",
    )
    THEORY_SECOND_HIGH_SCHOOL = "theory_second_high_school", "متوسطه دوم-نظری"
    EXCEPTIONAL_SECOND_HIGH_SCHOOL = "exceptional_second_high_school", "متوسطه دوم استثنائی"
    TECHNICAL_SECOND_HIGH_SCHOOL = "technical_second_high_school", "متوسطه دوم-هنرستان فنی"
    EXCEPTIONAL_TECHNICAL_SECOND_HIGH_SCHOOL = (
        "exceptional_technical_second_high_school",
        "فنی استثنائی",
    )
    PROFESSIONAL_SECOND_HIGH_SCHOOL = (
        "professional_second_high_school",
        "متوسطه دوم-هنرستان حرفه ای",
    )
    EXCEPTIONAL_PROFESSIONAL_SECOND_HIGH_SCHOOL = (
        "exceptional_professional_second_high_school",
        "حرفه ای استثنائی",
    )
    AGRICULTURE_SECOND_HIGH_SCHOOL = "agriculture_second_high_school", "متوسطه دوم-هنرستان کشاورزی"
    DEFT_SECOND_HIGH_SCHOOL = "deft_second_high_school", "متوسطه دوم-هنرستان کاردانش"
    EXCEPTIONAL_DEFT_SECOND_HIGH_SCHOOL = "exceptional_deft_second_high_school", "کاردانش استثنائی"
    THEORY_YEAR_HIGH_SCHOOL = "theory_year_high_school", "متوسطه سالی واحدی-نظری"
    PRE_UNIVERSITY = "pre_university", "پیش دانشگاهی"
    UNKNOWN = "unknown", "نامشخص"


class MemberShipTypeNameChoice(TextChoices):
    AID_COMMITTEE = "aid_committee", "کمیته امداد"
    REHABILITATION = "rehabilitation", "بهزیستی"
    SHAHID_FOUNDATION = "shahid_foundation", "بنیاد شهید"


class PolicyTermChoice(TextChoices):
    ONE_YEAR = "one_year", "یک سال"


class RequestSourceChoice(TextChoices):
    APP = "app", "اپ"
    PWA = "pwa", "pwa"


class PaymentStatusLogChoice(TextChoices):
    PENDING = "pending", "در انتظار پرداخت"
    PAID = "paid", "پرداخت شده"
    FAILED = "failed", "پرداخت ناموفق"
    CANCELED = "canceled", "انصراف از پرداخت"
    UNKNOWN = "unknown", "نامشخص"


class OrderPaymentStatusChoice(TextChoices):
    PENDING = "pending", "در انتظار پرداخت"
    PAID = "paid", "پرداخت شده"


class OrderStatusChoice(TextChoices):
    CREATION_REQUEST = "creation_request", "در حال ثبت درخواست"
    NEED_TO_ACCEPTED = "need_to_accepted", "در انتظار تایید درخواست"
    ACCEPTED_ORDER_BY_SCHOOL = "accepted_order_by_school", "تایید شده توسط مدرسه"
    ACCEPTED_ORDER_BY_ADMIN = "accepted_order_by_admin", "تایید شده توسط مدیر سامانه"
    REJECTED_ORDER_BY_SCHOOL = "rejected_order_by_school", "رد شده توسط مدرسه"
    REJECTED_ORDER_BY_ADMIN = "rejected_order_by_admin", "رد شده توسط مدیر سامانه"


class TransferRequestChoice(TextChoices):
    TRANSFER_REQUEST = "transfer_request", "ثبت درخواست انتقال"
    TRANSFER = "transfer", "منتقل شده"


class InsurancePurchaseOrderStatusLogChoice(TextChoices):
    CREATION_REQUEST = "creation_request", "در حال ثبت درخواست"
    NEED_TO_ACCEPTED = "need_to_accepted", "در انتظار تایید درخواست"
    ACCEPTED_ORDER_BY_SCHOOL = "accepted_order_by_school", "تایید شده توسط مدرسه"
    ACCEPTED_ORDER_BY_ADMIN = "accepted_order_by_admin", "تایید شده توسط مدیر سامانه"
    REJECTED_ORDER_BY_SCHOOL = "rejected_order_by_school", "رد شده توسط مدرسه"
    REJECTED_ORDER_BY_ADMIN = "rejected_order_by_admin", "رد شده توسط مدیر سامانه"
    TRANSFER_REQUEST = "transfer_request", "ثبت درخواست انتقال"
    TRANSFER = "transfer", "منتقل شده"
    PENDING = "pending", "در انتظار پرداخت"
    PAID = "paid", "پرداخت شده"


class SmsServicePanelNameChoices(TextChoices):
    PISHGAMRAYAN = "PSH", "پیشگام رایان"
    MEDIANA = "MED", "مدیانا"


class InsuranceTypeChoice(TextChoices):
    STUDENT_INCIDENTS = "student_incidents", "حوادث دانش آموزی"


class PaymentTypeChoices(TextChoices):
    PURCHASE_STUDENT_ACCIDENT_INSURANCE = "purchase_student_accident_insurance", "خرید بیمه حوادث دانش آموزی"
