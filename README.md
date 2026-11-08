# http proxy

Простой многопоточный HTTP прокси сервер

# Стек технологий

- Python
- Socket, Threading, Logging


# Как запустить

```
curl -s -x http://localhost:8888 http://example.com/
```
http://example.com/ - адрес сайта который требуется посетить (поддерживаются только сайты на порту 80, т.е. исключительно http протокол)

# Планы на будущее
- Реализация https прокси
- Реализация socks5
