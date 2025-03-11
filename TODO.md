# TODO
1. create a superuser with:
    * email: me@me.me
    * username: me
    * password: me

## Create Adaptation model - 50 points
1. create a new model called Adaption to represent adaptations of a book to another media type, e.g. movie, TV series, or board game. an adaptation should have:
    1. title (maximum length of 200)
    2. media_type
        * make it a single char field, for which the only CHOICES are: movie, TV series, board game. each of these must be represented by the lowercase initial letter of the media type m,t,b
    3. release_date
    4. book (relationship to the Book model instance that this adaptation is based on)
    5. creator (a relationship to the Author model. your Adaptation model should expect that there could be multiple creators for an Adaptation, but LIKE GENRE ON A BOOK, name this property in the singular form)
    6. have this class's string representation be the title of the adaptation
1. create the migration(s) for this model
1. make it so that the django admin site provides a way to add and edit Adaptations
1. login to the admin site
1. create a few Adaptations

## Create Views - 40 points

I'm providing the linked screenshots below not because your results must look exactly like mine, but just to help illustrate and possibly clarify the following instructions.

1. make it so that the url /catalog will additionally display the total number of adaptations in the system (see [docs/index.png](docs/index.png))
2. make it so that the url /catalog will additionally display the number of adaptations in the system for each of the 3 media types (see [docs/index.png](docs/index.png))
3. make it so that the url /catalog will additionally display the book with the most adaptations in the system (see [docs/index.png](docs/index.png))
4. make it so that the url /catalog/adaptations will list all the adaptations in this system  (see [docs/all-adapt.png](docs/all-adapt.png))
5. make it so that the url /catalog/adaptation/<id> will show the details of a single adaptation (see [docs/single-adapt.png](docs/single-adapt.png))
6. update the sidebar to include a link to the adaptations page (as in [docs/index.png](docs/index.png))

## Submit - 10 points
1. stage and commit your changes (INCLUDING TO THE `db.sqlite3` file)
1. push your changes to your github repository