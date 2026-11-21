SELECT 'categories' AS table_name, COUNT(*) AS row_count FROM categories
UNION ALL
SELECT 'authors', COUNT(*) FROM authors
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'books', COUNT(*) FROM books
UNION ALL
SELECT 'book_authors', COUNT(*) FROM book_authors
ORDER BY table_name;

SELECT
    b.book_id,
    b.title,
    b.publication_year,
    c.name AS category_name,
    COALESCE(string_agg(a.full_name, ', ' ORDER BY a.author_id), '(none)') AS authors
FROM books AS b
INNER JOIN categories AS c
    ON b.category_id = c.category_id
LEFT JOIN book_authors AS ba
    ON b.book_id = ba.book_id
LEFT JOIN authors AS a
    ON ba.author_id = a.author_id
GROUP BY b.book_id, b.title, b.publication_year, c.name
ORDER BY b.book_id;

SELECT COUNT(*) AS broken_category_links
FROM books AS b
LEFT JOIN categories AS c
    ON b.category_id = c.category_id
WHERE c.category_id IS NULL;