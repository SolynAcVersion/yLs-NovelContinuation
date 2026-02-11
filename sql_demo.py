import db_manager


def main():
    db = db_manager.NovelDB("demo.db")
    db.connect()

    db.create_new_table()

    char1 = {"id": "P001", "name": "yLD", "core_personality": "goooooooood"}
    db.add("characters", char1)

    all_chars = db.read("characters")
    one_char = db.read("characters", "P001")

    print(all_chars)
    print(one_char)

    update_data = {"relationship_network": "a<->b"}

    db.update("characters", "P001", update_data)
    all_chars = db.read("characters")
    one_char = db.read("characters", "P001")

    print(all_chars)
    print(one_char)

    db.close()


if __name__ == "__main__":
    main()
