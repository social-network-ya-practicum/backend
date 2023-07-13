import re

from django.core.exceptions import ValidationError

patterns = {
    'latin_lower': 'a-z',
    'latin_upper': 'A-Z',
    'numeric': '0-9',
    'special': '!./,',
}

pattern_all = ''
for key in patterns:
    pattern_all += patterns[key]


class ValidSymbolsPasswordValidator:
    """
    Validate whether the password contains only
    latin symbols (lowcase, uppercase), digits and special symbols.
    """

    message = (
        'Пароль должен состоять только из латинских букв(заглавных и строчных)'
        f", цифр и специальных символов ({patterns['special']})."
    )

    def validate(self, password, user=None):
        if re.search(f'[^{pattern_all}]', password):
            raise ValidationError(self.message)

    def get_help_text(self):
        return self.message


class RequiredSymbolsPasswordValidator:
    """
    Validate whether the password contains minimum one uppercase,
    one lowercase and one digit symbol.
    """

    message = (
        'Пароль должен содержать как минимум 1 заглавную, '
        '1 строчную латинскую букву и 1 цифру.'
    )

    def validate(self, password, user=None):
        for key in patterns:
            if key in ['latin_lower', 'latin_upper', 'numeric']:
                if re.search(f'[{patterns[key]}]', password) is None:
                    raise ValidationError(self.message)

    def get_help_text(self):
        return self.message
