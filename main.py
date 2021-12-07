from pprint import pprint
import csv
import re


def fix_number(phones):
    list_phones = []
    for i in phones[1:]:
        list_phones.append(i[5])

    new_phones = []
    pattern = r'(\+7|8)\s*\(*(\d{3})\)*\s*-*(\d{3})-*(\d{2})-*(\d{2})\s*(\(*(\w{3}\.)*\s(\d{4})+\)*)*'
    new_pattern = r'+7(\2)\3-\4-\5 \7\8'
    for i in list_phones:
        if i:
            result = re.sub(pattern, new_pattern, i)
            new_phones.append(result.rstrip())
        else:
            new_phones.append(i)

    for count, i in enumerate(phones[1:]):
        i[5] = new_phones[count]
    return phones


def fix_names(names):
    for i in names[1:]:
        for count, k in enumerate(i[:3]):
            result = re.findall(r'\w+\S', k)
            if len(result) == 3:
                i[0] = result[0]
                i[1] = result[1]
                i[2] = result[2]
            elif len(result) == 2 and count == 0:
                i[0] = result[0]
                i[1] = result[1]
            elif len(result) == 2 and count == 1:
                i[1] = result[0]
                i[2] = result[1]
    return names


def merge(data):
    exit_flag = False
    for count, i in enumerate(data[1:]):
        if exit_flag:
            break
        count2 = 0
        surname, first_name = data[1:][count][0], data[1:][count][1]
        for count3, k in enumerate(data[1:]):
            if k[0] == surname and k[1] == first_name and count2 < 1:
                count2 += 1
                continue
            elif k[0] == surname and k[1] == first_name and count2 >= 1:
                two_count = 0
                for h, m in zip(data[1:][count], k):
                    if h == '' and m != '':
                        data[count + 1][two_count] = m
                    two_count += 1
                if count3 + 2 == len(data):
                    del data[count3 + 1]
                    exit_flag = True
                    break
                del data[count3 + 1]
    return data


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    # pprint(contacts_list)

    contacts_list = fix_number(contacts_list)
    contacts_list = fix_names(contacts_list)
    contacts_list = merge(contacts_list)

    for i in contacts_list[1:]:
        print(i)

    with open("phonebook.csv", "w") as f:
        datawriter = csv.writer(f, delimiter=',', lineterminator='\r')
        datawriter.writerows(contacts_list)
