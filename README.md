# FacebookAuthorizTest
Тестирование авторизации  
The test it's getting cookie and use it next session if cookie be correct to save   
You can use command:  
pytest -v -s -m smoke --tb=line --reruns (n) --browser_name=chrome test_facebook.py  
pytest -v -s -m smoke test_facebook.py  
pytest -v -s test_facebook.py  
pytest test_facebook.py  
p.s reruns(n - number of reruns test)  
