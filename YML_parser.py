import xml.etree.ElementTree as ET
import requests
import json

# GLOBAL VARS
reqinfo = ["name", "company", "url", "platform", "version", "agency", "email"]


# TODO: написать запрос YML-файла с сервера
def getyml() -> str:
    # url = "https://anbik.ru/yml/YML_new.xml"
    # response =  requests.get(url)
    # with open("yml_anbik.xml", "wb") as f:
    #     f.write(response.content)
    xmlfile = 'yml_anbik.xml'
    return xmlfile


def parse_shopinfo_yml(xmlfile):
    data = {}
    arrdel = []
    arrpick = []
    currencies = {}
    categories = {}
    delivery = "None"
    pickup = "None"
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    data["date"] = root.attrib.get("date")
    
    for item in reqinfo:
        for elem in root.findall("shop"):
            if elem.find(item) is None:
                data[item] = 0
            else:
                data[item] = elem.find(item).text
            for elem2 in elem.findall('categories'):
                for elem3 in elem2.findall('category'):
                    if elem3.attrib.get("id") is not None and elem3.text is not None:
                        arr = []
                        if elem3.attrib.get("parentId") is not None:
                            arr.append(elem3.attrib.get("parentId"))
                        else:
                            arr.append(None)
                        arr.append(elem3.text)
                        categories[elem3.attrib.get("id")] = arr

    for elem in root.iter("currency"):
        if elem.attrib.get("id") is not None and elem.attrib.get("rate") is not None:
            currencies[elem.attrib.get("id")] = elem.attrib.get("rate")

    for elem in root.findall("shop"):
        for elem2_1 in elem.findall('delivery'):
            delivery = elem2_1.text
        for elem2_2 in elem.findall('pickup'):
            pickup = elem2_2.text
        for elem2_3 in elem.findall("delivery-options"):
            for elem2_3_1 in elem2_3.findall("option"):
                arrdel = [elem2_3_1.attrib.get("cost"), elem2_3_1.attrib.get("days")]
        for elem2_3 in elem.findall("pickup-options"):
            for elem2_3_2 in elem2_3.findall("option"):
                arrpick = [elem2_3_2.attrib.get("cost"), elem2_3_2.attrib.get("days")]
        if delivery != "false" and pickup != "false":
            if len(arrdel) != 0 and len(arrpick) != 0:
                data["delivery"] = arrdel
                data["pickup"] = arrpick
            elif (delivery != "false" or len(arrdel) != 0) and (pickup == "false" or pickup == 'None' or len(arrpick) != 0):
                data["delivery"] = arrdel
                if pickup == 'None':
                    data["pickup"] = "false"
                else:
                    data["pickup"] = pickup
            elif (delivery == "false" or delivery == 'None' or len(arrdel) != 0) and (pickup != "false" or len(arrpick) != 0):
                if delivery == 'None':
                    data["delivery"] = "false"
                else:
                    data["pickup"] = arrpick
        else:
            data["delivery"] = delivery
            data["pickup"] = pickup

    data["currencies"] = currencies
    data["categories"] = categories
    return data


def parse_offersinfo_yml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    arr = ['delivery-options', 'pickup-options', 'param']
    offers = []
    for elem0 in root.findall("shop"):
        for elem1 in elem0.findall("offers"):
            for elem2 in elem1:
                offer = {}
                offerinfo = {"bid": elem2.attrib.get("bid")}
                for elem3 in elem2:
                    if elem3.tag in arr:
                        if elem3.tag == 'param':
                            param = {elem3.attrib.get("name"): elem3.text}
                            offerinfo[elem3.tag] = param
                        else:
                            for elem4 in elem3:
                                offerinfo[elem3.tag] = elem4.attrib
                    else:                    
                        offerinfo[elem3.tag] = elem3.text
                offer[elem2.attrib.get("id")] = offerinfo
                offers.append(offer)
    return offers


def main():
    xmlfile = getyml()
    x = parse_shopinfo_yml(xmlfile)
    y = parse_offersinfo_yml(xmlfile)
    X = {'X': x}
    Y = {'Y': y}
    with open("info.txt", "w") as f:
        f.write(json.dumps(X))
    with open("offers.txt", "w") as f:
        f.write(json.dumps(Y))


main()
