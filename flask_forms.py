from wtforms.validators import InputRequired, DataRequired, Length, NumberRange
from flask_wtf import FlaskForm

from consts import (
    TextConsts,
    ChoiceFrameConsts,
    ChoiceIsBeershevaResidentConsts,
    ChoiceGenderConsts,
    ChoiceServicesConsts
)

from wtforms import (
    StringField,
    SubmitField,
    SelectField,
    IntegerField,
    RadioField,
    StringField,
    PasswordField
)


# A new building form. There are some requirments which apply on the input. Please read the flask documentation for more validators.
# Please notice that not all the inputs are a flask form and some are individual input which being dealt with the server purely
class NewBuildingForm(FlaskForm):
    title = IntegerField(
        TextConsts.TEXT_BUILDING_FIELD.value,
        validators=[
            InputRequired(TextConsts.TEXT_INPUT_REQUIRED.value),
            DataRequired(TextConsts.TEXT_DATA_REQUIRED.value),
            NumberRange(
                min=1, max=99999999, message=TextConsts.TEXT_BUILDING_DATA_INVALID.value
            ),
        ],
    )
    submit = SubmitField(TextConsts.TEXT_SAVE_CHANGES.value)


# A new apartment form. There are some requirments which apply on the input. Please read the flask documentation for more validators.
# Please notice that not all the inputs are a flask form and some are individual input which being dealt with the server purely
class NewApartmentForm(FlaskForm):
    apt_id = IntegerField(
        TextConsts.TEXT_APARTMENT_FIELD.value,
        validators=[
            InputRequired(TextConsts.TEXT_INPUT_REQUIRED.value),
            DataRequired(TextConsts.TEXT_DATA_REQUIRED.value),
            NumberRange(
                min=1,
                max=99999999,
                message=TextConsts.TEXT_APARTMENT_DATA_INVALID.value,
            ),
        ],
    )


# A new resident form. There are some requirments which apply on the input. Please read the flask documentation for more validators.
# Please notice that not all the inputs are a flask form and some are individual input which being dealt with the server purely
class NewResidentForm(FlaskForm):
    field_validators = [InputRequired(TextConsts.TEXT_INPUT_REQUIRED.value)]
    full_name_field = StringField(
        TextConsts.TEXT_FULL_NAME_FIELD.value,
        [
            InputRequired(TextConsts.TEXT_INPUT_REQUIRED.value),
            Length(min=2, max=25, message=TextConsts.TEXT_STRING_DATA_INVALID.value),
        ],
    )

    frame_selection_field = SelectField(
        "Frame",
        choices=[
            (association.value, association.value) for association in ChoiceFrameConsts
        ],
        validators=field_validators,
    )

    select_gender_field = RadioField(
        TextConsts.TEXT_GENDER_FIELD.value,
        choices=[(gender.value, gender.value) for gender in ChoiceGenderConsts],
        validators=field_validators,
    )

    select_service_field = SelectField(
        TextConsts.TEXT_SERVICE_FIELD.value,
        choices=[(service.value, service.value) for service in ChoiceServicesConsts],
        validators=field_validators,
    )

    is_beersheva_selection_field = SelectField(
        TextConsts.TEXT_IS_BEERSHEVA_RESIDENT_FIELD.value,
        choices=[
            (is_beersheva.value, is_beersheva.value)
            for is_beersheva in ChoiceIsBeershevaResidentConsts
        ],
        validators=field_validators,
    )

    taz_field = StringField(
        TextConsts.TEXT_FULL_NAME_FIELD.value,
        [Length(min=7, max=9, message=TextConsts.TEXT_STRING_DATA_INVALID.value)],
    )

    submit = SubmitField(TextConsts.TEXT_SAVE_CHANGES.value)


class NewUserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    submit = SubmitField("Sign in")