from gitstory.common_fun.date_time import import_mmddyyyy  
from datetime import date
from pytest import raises

class TestDateTime:
    def test_import_mmddyyyy(self):
        assert(import_mmddyyyy("12-1-2024") == date(2024, 12, 1) )
        assert(import_mmddyyyy("05-18-2006") == date(2006, 5, 18) )
        assert(import_mmddyyyy("3-28-1984") == date(1984, 3, 28) ) 

        with raises(ValueError):
            import_mmddyyyy("this can't be valid")

        with raises(ValueError):
            import_mmddyyyy("0-1.15-5")
        with raises(ValueError):
            import_mmddyyyy("12012024")
        with raises(ValueError):
            import_mmddyyyy("12-01-2024-")
        with raises(ValueError):
            import_mmddyyyy("12-012024")
        with raises(ValueError):
            import_mmddyyyy("0-28-2024")
        with raises(ValueError):
            import_mmddyyyy("13-28-2024")
        with raises(ValueError):
            import_mmddyyyy("12-0-2024")
        with raises(ValueError):
            import_mmddyyyy("12-33-2024")