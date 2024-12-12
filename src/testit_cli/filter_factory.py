import typing

from .models.config import Config


class FilterFactory:
    @classmethod
    def get(cls, config: Config, external_keys: typing.List[str]) -> str:
        initialization = {
            'pytest': cls.__initialize_pytest_filter,
            'robotframework': cls.__initialize_robotframework_filter,
            'behave': cls.__initialize_behave_filter,
            'nose': cls.__initialize_nose_filter,
            'gradle-testng': cls.__initialize_gradle_testng_junit4_junit5_filter,
            'gradle-junit4': cls.__initialize_gradle_testng_junit4_junit5_filter,
            'gradle-junit5': cls.__initialize_gradle_testng_junit4_junit5_filter,
            # 'gradle-jbehave': cls.__initialize_jbehave_filter,
            'gradle-cucumber': cls.__initialize_cucumber_cucumberjs_jest_golang_filter,
            'maven-testng': cls.__initialize_maven_testng_junit4_junit5_filter,
            'maven-junit4': cls.__initialize_maven_testng_junit4_junit5_filter,
            'maven-junit5': cls.__initialize_maven_testng_junit4_junit5_filter,
            # 'maven-jbehave': cls.__initialize_jbehave_filter,
            'maven-cucumber': cls.__initialize_cucumber_cucumberjs_jest_golang_filter,
            'cucumberjs': cls.__initialize_cucumber_cucumberjs_jest_golang_filter,
            'codeceptjs': cls.__initialize_codeceptjs_mocha_playwright_filter,
            'jest': cls.__initialize_cucumber_cucumberjs_jest_golang_filter,
            'mocha': cls.__initialize_codeceptjs_mocha_playwright_filter,
            'playwright': cls.__initialize_codeceptjs_mocha_playwright_filter,
            'mstest': cls.__initialize_mstest_nunit_xunit_filter,
            'nunit': cls.__initialize_mstest_nunit_xunit_filter,
            'xunit': cls.__initialize_mstest_nunit_xunit_filter,
            'specflow': cls.__initialize_specflow_filter,
            'golang': cls.__initialize_cucumber_cucumberjs_jest_golang_filter,
        }

        return initialization[config.framework](external_keys)

    @classmethod
    def __initialize_pytest_filter(cls, external_keys: typing.List[str]):
        """Initialize filter for pytest run"""
        return '-k\n' + ' or '.join(external_keys)

    @staticmethod
    def __initialize_robotframework_filter(external_keys: typing.List[str]):
        """Initialize filter for RobotFramework run"""
        robotframework_filter = ""

        for external_key in external_keys:
            robotframework_filter += '-t' + external_key.replace(" ", "") + '\n'

        return robotframework_filter

    @staticmethod
    def __initialize_behave_filter(external_keys: typing.List[str]):
        """Initialize filter for Behave run"""
        return '-n' + '|'.join(external_keys)

    @classmethod
    def __initialize_nose_filter(cls, external_keys: typing.List[str]):
        """Initialize filter for Nose run"""
        return ' '.join(external_keys)

    @staticmethod
    def __initialize_gradle_testng_junit4_junit5_filter(external_keys: typing.List[str]):
        """Initialize filter for gradle TestNG or JUnit4 or JUnit5 run with gradle"""
        autotest_keys = []

        for external_key in external_keys:
            autotest_keys.append('--tests ' + external_key)

        return ' '.join(autotest_keys)

    # @classmethod
    # def __initialize_jbehave_filter(cls, external_keys: typing.List[str]):
    #     """Initialize filter for JBehave run"""
    #     return '+' + ' '.join(external_keys)

    @staticmethod
    def __initialize_maven_testng_junit4_junit5_filter(external_keys: typing.List[str]):
        """Initialize filter for TestNG or JUnit4 or JUnit5 run with maven"""
        autotest_keys = []

        for external_key in external_keys:
            autotest_keys.append('-Dtest=' + external_key)

        return ' '.join(autotest_keys)

    @classmethod
    def __initialize_codeceptjs_mocha_playwright_filter(cls, external_keys: typing.List[str]):
        """Initialize filter for CodeceptJS or Mocha or Playwright run"""
        return '|'.join(external_keys)

    @classmethod
    def __initialize_cucumber_cucumberjs_jest_golang_filter(cls, external_keys: typing.List[str]):
        """Initialize filter for Cucumber or CucumberJS or Jest or Golang run"""
        autotest_keys = []

        for external_key in external_keys:
            autotest_keys.append('^' + external_key + '$')

        return '|'.join(autotest_keys)

    @staticmethod
    def __initialize_mstest_nunit_xunit_filter(external_keys: typing.List[str]):
        """Initialize filter for MSTest or NUnit or XUnit run"""
        autotest_keys = []

        for external_key in external_keys:
            autotest_keys.append('FullyQualifiedName=' + external_key)

        return '|'.join(autotest_keys)

    @staticmethod
    def __initialize_specflow_filter(external_keys: typing.List[str]):
        """Initialize filter for SpecFlow run"""
        autotest_keys = []

        for external_key in external_keys:
            autotest_keys.append('FullyQualifiedName~' + external_key)

        return '|'.join(autotest_keys)
