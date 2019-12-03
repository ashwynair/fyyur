from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField,\
    DateTimeField, BooleanField
from wtforms.validators import DataRequired, URL, ValidationError, Optional


def validate_number(form, field):
    phone_dict = {
        "AL": [205, 251, 256, 334, 659, 938],
        "AK": [907],
        "AZ": [480, 520, 602, 623, 928],
        "AR": [327, 479, 501, 870],
        "CA": [209, 213, 310, 323, 341, 369, 408, 415, 424, 442, 510, 530, 559,
               562, 619, 626, 627, 628, 650, 657, 661, 669, 707, 714, 747, 752,
               760, 764, 805, 818, 831, 858, 909, 916, 925, 935, 949, 951],
        "CO": [303, 719, 720, 970],
        "CT": [203, 475, 860, 959],
        "DE": [302],
        "DC": [202],
        "FL": [239, 305, 321, 352, 386, 407, 561, 689, 727, 754, 772, 786, 813,
               850, 863, 904, 927, 941, 954],
        "GA": [229, 404, 470, 478, 678, 706, 762, 770, 912],
        "HI": [808],
        "ID": [208],
        "IL": [217, 224, 309, 312, 331, 447, 464, 618, 630, 708, 730, 773, 779,
               815, 847, 872],
        "IN": [219, 260, 317, 574, 765, 812, 930],
        "IA": [319, 515, 563, 641, 712],
        "KS": [316, 620, 785, 913],
        "KY": [270, 364, 502, 606, 859],
        "LA": [225, 318, 337, 504, 985],
        "ME": [207],
        "MD": [227, 240, 249, 280, 301, 410, 443, 667],
        "MA": [339, 351, 413, 508, 617, 774, 781, 857, 978],
        "MI": [231, 248, 269, 278, 313, 517, 586, 616, 679, 734, 810, 906, 947,
               989],
        "MN": [218, 320, 507, 612, 651, 763, 952],
        "MS": [228, 601, 662, 769],
        "MO": [314, 417, 557, 573, 636, 660, 816, 975],
        "MT": [406],
        "NE": [308, 402],
        "NV": [702, 725, 775],
        "NH": [603],
        "NJ": [201, 551, 609, 732, 848, 856, 862, 908, 973],
        "NM": [505, 575, 957],
        "NY": [212, 315, 347, 516, 518, 585, 607, 631, 646, 716, 718, 845, 914,
               917],
        "NC": [252, 336, 704, 828, 910, 919, 980, 984],
        "ND": [701],
        "OH": [216, 220, 234, 283, 330, 380, 419,
               440, 513, 567, 614, 740, 937],
        "OK": [405, 580, 918],
        "OR": [458, 503, 541, 971],
        "PA": [215, 267, 272, 412, 445, 484, 570, 582, 610, 717, 724, 814, 835,
               878],
        "RI": [401],
        "SC": [803, 843, 854, 864],
        "SD": [605],
        "TN": [423, 615, 629, 731, 865, 901, 931],
        "TX": [210, 214, 254, 281, 325, 346, 361, 409, 430, 432, 469, 512, 682,
               713, 737, 806, 817, 830, 903, 915, 936, 940, 956, 972, 979],
        "UT": [385, 435, 801],
        "VT": [802],
        "VA": [276, 434, 540, 571, 703, 757, 804],
        "WA": [206, 253, 360, 425, 509, 564],
        "WV": [304, 681],
        "WI": [262, 274, 414, 534, 608, 715, 920],
        "WY": [307]
    }

    if int(field.data[:3]) not in phone_dict[form.state.data]:
        print("First three characters are: " + str(field.data[3]))
        print("Chosen state: " + str(phone_dict[form.state.data]))
        raise ValidationError("Please enter a valid area code for {}"
                              .format(form.state.data))


class ShowForm(FlaskForm):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default=datetime.today()
    )


class VenueForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    address = StringField(
        'address', validators=[DataRequired()]
    )
    phone = StringField(
        'phone', validators=[validate_number]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
    genres = SelectMultipleField(
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[Optional(), URL()]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    website = StringField(
        'website', validators=[Optional(), URL()]
    )


class ArtistForm(FlaskForm):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone', validators=[validate_number]
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )
    seeking_description = StringField(
        'seeking_description'
    )
    website = StringField(
        'website', validators=[Optional(), URL()]
    )
    image_link = StringField(
        'image_link', validators=[Optional(), URL()]
    )
