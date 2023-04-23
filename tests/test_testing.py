import pytest
from calc import add, Bank, InsufincentFunds

@pytest.fixture
def bank_init():
    #run code before test
    yield Bank()
    #run code after test finishes
@pytest.fixture
def bank_a_init():
    return Bank(50)

@pytest.mark.parametrize("num1, num2, exp", [(3,5,8),(1,1,2),(6,5,11)])
def test_add(num1, num2, exp):
    assert add(num1,num2) == exp 

def test_bank_set_initial(bank_a_init):
    assert bank_a_init.balance == 50

def test_bank_default(bank_init):
    assert bank_init.balance == 0

def test_withdraw(bank_a_init):
    bank_a_init.widhdraw(20)
    assert bank_a_init.balance == 30

def test_deposit(bank_a_init):
    bank_a_init.deposit(30)
    assert bank_a_init.balance == 80

def test_collect(bank_a_init):
    bank_a_init.collect()
    assert round(bank_a_init.balance,6) == 55

@pytest.mark.parametrize("dep, wit, balance", [(2,1,1), (300,200,100)])
def test_bank_transaction(bank_init, dep, wit, balance):
    bank_init.deposit(dep)
    bank_init.widhdraw(wit)
    assert bank_init.balance == balance

def test_infufince_funds(bank_init):
    with pytest.raises(InsufincentFunds):
        bank_init.widhdraw(100)
