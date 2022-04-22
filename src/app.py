from database import Writer, Reader, DocumentUpdater, DocumentRemover
import pandas as pd
import numpy as np


def main():
    df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar',
                             'foo', 'bar', 'foo', 'foo'],
                       'B': ['one', 'one', 'two', 'three',
                             'two', 'two', 'one', 'three'],
                       'C': np.random.randn(8), 'D': np.random.randn(8)})

    writer = Writer("test1", "chunks_write")

    chunks_number = 2
    chunk_size = df.shape[0]//chunks_number # here might be a miscalculation but it's only for template presentation of wirting chunks
    for i in range(chunks_number):
        writer.add_dataset(df[i * chunk_size:(i + 1) * chunk_size])


if __name__ == '__main__':
    main()
