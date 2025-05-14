"""
Provider for faker to generate E164 compatible phone numbers.

"safe_numbers" provided by https://fakenumber.org/,
 the GB/United Kingdom "safe_numbers" are reported as invalid by the phonenumbers package.

Adapted from https://github.com/crowdcomms/faker-e164/blob/dc5bb604d39beb62b98e46f7f19f246118830c14/faker_e164/providers.py
"""

import phonenumbers
from faker.providers import BaseProvider
from phonenumbers import PhoneNumber

__all__ = ("E164Provider",)

safe_numbers = {
    "AU": [
        "+61491570156",
        "+61491570157",
        "+61491570158",
        "+61491570159",
        "+61491570110",
    ],
    "US": [
        "+12025550191",
        "+12025550188",
        "+12025550187",
        "+12025550137",
        "+12025550105",
        "+12025550124",
    ],
    "GB": [
        "+441632960600",
        "+441632960541",
        "+441632960702",
        "+441632960979",
        "+441632960570",
        "+441632960864",
    ],
    "CA": [
        "+16135550110",
        "+16135550120",
        "+16135550109",
        "+16135550151",
        "+16135550136",
        "+16135550119",
    ],
}


class E164Provider(BaseProvider):
    """
    Provider to generate random phone numbers for various countries

    >>> from faker import Faker
    >>> from core.faker_providers import E164Provider
    >>> fake = Faker()
    >>> fake.add_provider(E164Provider)
    >>> phone_number = fake.e164()

    # To fake an e164 phone number
    >>> fake.e164(region_code="AU", valid=True, possible=True)

    # To fake a "safe" e164 phone number from a number of selected regions
    >>> fake.safe_e164(region_code="US")
    """

    _e164_numerify_pattern = "%######!!!!!!!!"  # https://en.wikipedia.org/wiki/E.164

    def _get_e164_numerify_pattern(
        self,
        region_code: str,
        is_possible=True,
    ):
        if not is_possible:
            return "#!!!!!!"

        country_code = phonenumbers.country_code_for_region(region_code)
        numerify_pattern = self._e164_numerify_pattern[len(str(country_code)) :]

        return f"{country_code}{numerify_pattern}"

    def _e164(
        self,
        region_code: str,
        is_valid=True,
        is_possible=True,
    ) -> PhoneNumber:
        """
        Generate an e164 phone number
        """
        if is_valid and not is_possible:
            msg = "is_valid must be False if is_possible is False"
            raise ValueError(msg)

        e164_numerify_pattern = self._get_e164_numerify_pattern(
            region_code,
            is_possible=is_possible,
        )
        phone_number = self.numerify(e164_numerify_pattern)

        while not isinstance(phone_number, PhoneNumber):
            try:
                phone_number = phonenumbers.parse(phone_number, region_code)
            except phonenumbers.phonenumberutil.NumberParseException:
                phone_number = self.numerify(e164_numerify_pattern)
                continue

            if is_valid != phonenumbers.is_valid_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue

            if is_possible != phonenumbers.is_possible_number(phone_number):
                phone_number = self.numerify(e164_numerify_pattern)
                continue

        return phone_number

    def e164(
        self,
        region_code: str | None = None,
        valid=True,
        possible=True,
    ) -> str:
        """
        Return a random e164 phone number
        """
        if region_code is None:
            region_code = self.random_element(phonenumbers.SUPPORTED_REGIONS)

        phone_number = self._e164(
            region_code,
            is_valid=valid,
            is_possible=possible,
        )

        return phonenumbers.format_number(
            numobj=phone_number,
            num_format=phonenumbers.PhoneNumberFormat.E164,
        )

    def safe_e164(
        self,
        region_code: str | None = None,
    ) -> str:
        """
        Return a random "safe" e164 phone number
        """
        if region_code is None:
            region_codes = list(safe_numbers.keys())
            region_code = self.random_element(region_codes)

        phone_numbers = safe_numbers[region_code]
        phone_number = phonenumbers.parse(self.random_element(phone_numbers))

        return phonenumbers.format_number(
            numobj=phone_number,
            num_format=phonenumbers.PhoneNumberFormat.E164,
        )

    def non_e164(
        self,
        *args,
        **kwargs,
    ) -> str:
        """
        Return a random non-e164 phone number
        """
        e164_phone_number = self.e164(*args, **kwargs)

        # TODO: Find a better way to generate non-e164 phone numbers
        return e164_phone_number[1:]
