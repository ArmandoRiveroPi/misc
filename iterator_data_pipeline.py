class MyIterator(object):

    def __init__(self):
        self.collection = list(range(100))
        self.position = 0
        self.max_position = len(self.collection)

    def __next__(self):
        if self.position >= self.max_position:
            raise StopIteration
        result = self.collection[self.position]
        self.position += 1
        return result

    def __iter__(self):
        return self

my_iter = MyIterator()
next(my_iter)
my_iter.__next__()


def my_iterator():
    for element in list(range(100)):
        yield element

my_iter = my_iterator()

for item in my_iter:
    print(item)
# a = range(100)
# for number in a:
#     print(number**2)

def generate_weird_numbers():
    for number in range(100):
        new_number = number + 10 * number
        yield new_number ** 2

def test_generator():
    start = 0
    max = 3
    while True:
        yield start
        start += 1
        if start >= max:
            return 33

my_gen = test_generator()

# for square in generate_weird_numbers():
#     print("The weird number is", square)
#
# for square in generate_weird_numbers():
#     print("The weird number is", square)


def generator_function(items):
    for item in items:
        new_item = str(item)
        new_item += " append string to the end "
        yield new_item


# for new_item in generator_function(items):
#     print(new_item)


def get_items_from_db(cursor, batch_size=100, offset=0):
    query = """
            SELECT item_val1, item_val2, item_val3
            FROM items_table
            where item is not null -- or whatever conditions
            order by item_val1 -- there must be a way of ordering the items
            limit {limit}
            offset {offset};
            """.format(
        limit=batch_size,
        offset=offset,
    )
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            yield format_item(row)

        # recursive call to keep extracting from the db
        further_items = get_items_from_db(cursor,
                              batch_size, offset + batch_size)
        yield from further_items

def string_transformation(items):
    for item in items:
        transformed_item = item.copy()
        transformed_item.string_content = \
            item.string_content.replace('old_string','new_string')
        yield transformed_item


def api_calling_transformation(items):
    batch_size = 100
    batch = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield from get_api_results(batch)
            batch = []
    # processing the remains
    yield from process_batch(batch)

items = generate_items()
transformed_items = transform_items(items)
final_items = Parallel(n_jobs=6)(delayed(lambda x: x)(item) for item in transformed_items)

if __name__ == '__main__':
    pass
