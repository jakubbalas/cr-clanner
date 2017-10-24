Clash Roayale Clan Stats
========================


How to run the project
----------------------

1) Clone this repo
2) `docker-compose up`
3) `docker-compose exec app db upgrade` if you don't have db source

The next step will be moved to admin once we have some  
`docker-compose exec app flask add_clan --tag=2Q0JYGJP --name="The AAA-Team"`


if you want to run the import manually, run  
`docker-compose exec app flask load_data`
