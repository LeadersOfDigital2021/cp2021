# Цифровой прорыв - 2021

Данный репозиторий является итоговым решением кейса Росатом в хакатоне "Цифровой прорыв - 2021".

Краткое описание проекта

Данное решение способно как распознавать существующую запись в mpeg4, так и обработать встречу онлайн, без необходимости записи (например, если запись невозможна из соображений безопасности). Решение сохраняет все распознанные записи в удобной структуре в виде встреч, в которых присутствует стенограмма встречи и протокол, составленный по стенограмме. Протокол можно скачать одним кликом для дальнейшего использования (например, загрузки в систему электронного документооборота для подписи). Система способна интегрироваться с почтовыми клиентами или другими системами для постановки встречи из календаря. Так же система легко интегрируется с системами электронного документооборота при наличии там API для интеграции.

Стек технологий

 - Unity - Ui, front-end 2020.3.16f
 - C++ (Kaldi) - распознавание речи (AI)
 - Python (Flask+SQLAlchemy) - back-end, database engine, NLP (AI)
 - SQLite - база данных (легко масштабируется в Postgres благодаря возможностям SQLAlchemy, но для MVP достаточно SQLite)
 - Python (Keras) - в итоговом прототипе не использовался из-за проблем в обучении (слишком мало данных) - NLP (AI)
 - Figma - Ux/Ui

Структура

 - Server - в этом разделе хранятся файлы для работы с сервером, NLP модель (AI) для поиска ключевых фраз для протокола и ML-ноутбук со структурой нейронной сети. Выполнен на языке Python. И kaldi для обучения распознавания языковых моделей.
 - Client - раздел содержит файлы для работы с ui частью проекта. Кроме того, здесь содержится ML модель для распознавания речи Kaldi.
