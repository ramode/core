SERVICE_TYPE = [
    ('internet', 'Internet'),
    ('iptv', 'TV'),
    ('web-user','WEB user')
    ]

DEBITING_METHOD_DAILY = 0
DEBITING_METHOD_MONTH_DAILY = 1
DEBITING_METHOD_MONTHLY = 2
DEBITING_METHOD_START = 3
DEBITING_METHOD_END = 4

DEBITING_METHODS = [
    (DEBITING_METHOD_DAILY,'daily'),
    (DEBITING_METHOD_MONTH_DAILY,'mounthdaily'),
    (DEBITING_METHOD_MONTHLY,'mounthly'),
    (DEBITING_METHOD_START,'start'),
    (DEBITING_METHOD_END,'end')
]

SERVICE_STATE = [
    (0,'on'), # доступна
    (1,'admin off'), # запрещенна админом, включается админом
    (2,'suspend'), # не включать при пополнении баланса, включается пользователем
    (3,'block') # включать при пополнении баланса
]

NAS_TYPE = [
    ('radius','Radius')
]

CASH_TYPE = [
    (0,'cash'),
    (1,'non-cash'),
    (2,'online'),
    (3,'bonus')
]
