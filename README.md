# bjj_tournaments
Это мой первый мини-проект, парсер, который я написал не по заданию на курсе или по видео с канала, а целиком сам. 

Проект писался для человека, который занимается бразильским джиу-джитсу и часто выступает на соревнованиях. Многие федерации которые проводили спортивные турниры в нашей стране ушли. Некоторые из них вернулись. Чтобы спортсменам было быстрее найти себе подходящий турнир, я собрал их все в одном месте. Не нужно проверять разные сайты федераций, кто-то вернулся, а потом опять ушел и т.д.

Приложение написано на Django. Главная страница имеет заголовок, рандомную новость из нашего спорта или цитату авторитетного тренера, цитата подгружается из бд sqlite и ссылку на страницу с поиском. На страничке с поиском нужно ввести свой город, если в городе, который указали, есть соревнования, то результат поиска их все отобразит одно за другим с сылкой на соответствующий сайт.
Приложение парсит 3 сайта, два из них с динамически подгружаемыми данными, по этому для их скрайпинга использовался Selenium.

В дальнейшем хочу оптимизировать приложение, чтобы код выполнялся асинхронно, что ускорит ожидание пользователя.

