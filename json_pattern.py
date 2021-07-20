def something(name, address, website, opening_hours, ypage, goods, reviews):
    data_grabbed = {
        "name": name,
        "address": address,
        "website": website,
        "opening_hours": [
            {
                "mon": opening_hours[0],
                "tue": opening_hours[1],
                "wed": opening_hours[2],
                "thu": opening_hours[3],
                "fri": opening_hours[4],
                "sat": opening_hours[5],
                "sun": opening_hours[6],
            }
        ],
        "ypage": ypage,
        "goods": goods,
        "reviews": reviews

    }
    return data_grabbed
