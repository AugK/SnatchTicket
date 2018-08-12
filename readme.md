### Purpose
In order to book swim ticket easily, this tool is developed. It's based on a popular open source tool called [Splinter]("http://splinter.readthedocs.io/en/latest/").

### Useage
At first, you should make sure the chrome driver is installed on your PC.

See [install guide]("http://splinter.readthedocs.io/en/latest/install.html") for details.

>run(user, password, url="http://www.wentiyun.cn/venue-722.html", choice="2", headless=False)

- Required: **user** indicates your account name. Make sure you have already registered.
- Required: **password** indicates the password, of course.
- Optional: **url** indicates the url of ticket-booking page.
- Optional: **choice** ranges from "1" to "7"(it's a string). **"choice=2"** means tomorrow and it's default.
- Optional: **headless** indicates the type of browser. It's headless browser when **headless=False** and it's default.

###Example
```python
from pkg_demo import demo
demo.run('13812345678', 'password')
# demo.run('13812345678', 'password', choice="1", headless=True)
```