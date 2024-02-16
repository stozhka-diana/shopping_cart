-- docker compose up -d
-- docker compose cp dump.sql database:dump.sql
-- docker compose exec -d database psql -U dev -p 5432 -d shopping_cart -f dump.sql

INSERT INTO public.products_category VALUES (1, 'Clothes', 1, 6, 2, 0, NULL);
INSERT INTO public.products_category VALUES (2, 'T-Shirts', 4, 5, 2, 1, 1);
INSERT INTO public.products_category VALUES (3, 'Pants', 2, 3, 2, 1, 1);
INSERT INTO public.products_category VALUES (4, 'Books', 1, 12, 1, 0, NULL);
INSERT INTO public.products_category VALUES (5, 'Classics', 2, 5, 1, 1, 4);
INSERT INTO public.products_category VALUES (6, 'Poem', 6, 11, 1, 1, 4);
INSERT INTO public.products_category VALUES (7, 'Ukranian', 9, 10, 1, 2, 6);
INSERT INTO public.products_category VALUES (9, 'English', 3, 4, 1, 2, 5);


INSERT INTO public.products_product VALUES (1, 'Kobzar', 'kobzar', 'The name of the first book-collection of poetic works of Taras Shevchenko in 1840.', 500, 4.5, 7);
INSERT INTO public.products_product VALUES (3, 'Lord of the Flies', 'lord-of-the-flies', 'The plot concerns a group of British boys who are stranded on an uninhabited island and their disastrous attempts to govern themselves.', 450, 4.3, 9);

