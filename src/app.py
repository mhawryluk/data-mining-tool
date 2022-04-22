from database import Reader


def main():
    reader = Reader("test1", "chunks_write")
    print(reader.get_nth_chunk({}, ["A", "B", "C"], chunk_size=3, chunk_number=4))


if __name__ == '__main__':
    main()
