# with open('../domains/internet/balance/train.txt', 'w') as result_file:
#     with open('../domains/internet/home_service/train.txt') as src1:
#             for l1 in src1.readlines():
#                 with open('../domains/internet/specify_hour/train.txt') as src2:
#                     for l2 in src2.readlines():
#                         result_file.write(l1.strip() + " і " + l2.strip() + '\n')
#                         #result_file.write(l1.strip() + " а також " + l2)

f1 = open('/home/max/bots/rus/provider-bot/provider_bot/domains/internet/check_balance/train.txt')
f2 = open('/home/max/bots/rus/provider-bot/provider_bot/domains/internet/home_service/train.txt')
res = open('/home/max/bots/rus/provider-bot/provider_bot/domains/internet/balance_and_home_service/train.txt', 'w')

for a, b in zip(f1.readlines(), f2.readlines()):
    res.write(a.strip() + " и " + b.strip() + '\n')

f1.close()
f2.close()
res.close()