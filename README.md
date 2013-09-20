# Registro Electoral Permanente Web Service

This is a flask application that serves the REP, which is publicly available [here](http://www.cne.gob.ve/web/registro_electoral_descarga/abril2012/nacional.php), as a web service. Mainly done out of boredom.

As it is right now, it lets clients fetch voter records by providing a document ID, voters from a specific voting center, and various stats of voting centers such as minium/maximum/average age as well as age distribution.

You can test this out without installing anything on [my installation](http://cne.dev.juanrebolledog.me/) by appending the desired endpoint to the URL, like so:

    http://cne.dev.juanrebolledog.me/voter/5892464

## API

### Voter

URL: /voter/:document_id

Returns the data of the specified voter

#### Example

    /voter/5892464

### Center Voters

URL: /voters/:center_id

Returns all voters registered in that specific center

#### Example

    /voters/70906017

### Center Stats

URL: /voters/:center_id/age/:calc_type

Returns stats from a specific voting center. Parameter calc_type can be 'min', 'max', 'avg', 'dist'.

#### Example

    /voters/70906017/age/avg

### Center Information

URL: /center/:center_id

Returns the details of a specified center

#### Example

    /center/70906017

### Center Search

URL: /centers

Returns the registered voting centers. Accepts three different filter arguments: 'state', 'municipality' and 'parish'.

#### Example

    /centers?state=7&municipality=9&parish=1
