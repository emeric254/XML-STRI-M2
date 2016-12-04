<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
    <xsl:template match="/">
        <html>
            <head>
              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"></link>
              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap-theme.min.css" integrity="sha384-rHyoN1iRsVXV4nD0JutlnGaslCJuC7uwjduW9SVrLvRYooPp2bWYgmgJQIXwl/Sp" crossorigin="anonymous"></link>
            </head>
            <body style="padding-top:70px; pading-bottom:30px;">
                <nav class="navbar navbar-inverse navbar-fixed-top">
                    <div class="container">
                        <div class="navbar-header">
                          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                            <span class="sr-only">Toggle navigation</span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                            <span class="icon-bar"></span>
                          </button>
                          <a class="navbar-brand" href="#">TP XML - Festival de Cannes</a>
                        </div>
                        <div id="navbar" class="navbar-collapse collapse">
                          <ul class="nav navbar-nav">
                            <li><a href="#">Introduction</a></li>
                            <li><a href="#films">Films</a></li>
                            <li><a href="#jury">Jury</a></li>
                            <li><a href="#palmares">Palmares</a></li>
                            <li><a href="#artistes">Artistes</a></li>
                          </ul>
                        </div><!--/.nav-collapse -->
                    </div>
                </nav>
                <div class="container theme-showcase" role="main">
                    <div class="jumbotron">
                        <p>
                            Chaque année, au mois de mai, le Festival de Cannes s’empare de la ville et des tabloïds du monde entier.
                            Des starlettes bronzant sur les plages, des stars gravissant le célèbre tapis rouge, 400 photographes mitraillant ces célébrités : ainsi s'ouvre la légende du Festival de Cannes.
                            Une fête où se repèrent les nouveaux talents, où sont sacrés les maîtres de l'image et où sont honorés les grands disparus.
                        </p>
                    </div>


                    <div class="page-header" id="films">
                        <h2>Liste des films présentés au festival</h2>
                    </div>
                    <xsl:for-each select="//film">
                        <xsl:sort select="titre"/>
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title">
                                    <xsl:value-of select="titre"/>
                                </h3>
                            </div>
                            <div class="panel-body">
                                <div class="row">
                                    <div class="col-md-4">
                                        <p>
                                            Année de production :
                                            <xsl:value-of select="@annee_production"/>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p>
                                            Date de sortie :
                                            <xsl:value-of select="@date_sortie"/>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p>
                                            Nationalités :
                                            <xsl:for-each select="@pays">
                                                <xsl:call-template name="afficherPays">
                                                    <xsl:with-param name="codePays" select="." />
                                                </xsl:call-template>
                                            </xsl:for-each>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p>
                                            Réalisé par :
                                            <xsl:for-each select="casting/@realisateurs">
                                                <xsl:call-template name="afficher_nom_artiste">
                                                    <xsl:with-param name="artiste_id" select="." />
                                                </xsl:call-template>
                                                <!-- detail artiste -->
                                            </xsl:for-each>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p>
                                            Mis en scène par :
                                            <xsl:for-each select="casting/@scenaristes">
                                                <xsl:call-template name="afficher_nom_artiste">
                                                    <xsl:with-param name="artiste_id" select="." />
                                                </xsl:call-template>
                                                <!-- detail artiste -->
                                            </xsl:for-each>
                                        </p>
                                    </div>

                                    <!-- -->
                                    <!-- -->
                                    <xsl:for-each select=".">
                                        <div class="col-md-12">
                                            <p>Prix obtenus :</p>
                                            <!-- liste prix du film -->
                                        </div>
                                    </xsl:for-each>
                                    <xsl:for-each select=".">
                                        <div class="col-md-12">
                                            <p>Prix obtenus par ses interpretes :</p>
                                            <!-- liste prix des artistes -->
                                        </div>
                                    </xsl:for-each>

                                    <div class="col-md-12">
                                        <p>Synopsis :</p>
                                        <p><xsl:value-of select="synopsis"/></p>
                                    </div>

                                    <div class="col-md-12">
                                        <p>Casting :</p>
                                        <xsl:for-each select="personnages/personnage">
                                            <p>
                                                <xsl:call-template name="afficher_nom_artiste">
                                                    <xsl:with-param name="artiste_id" select="@incarne_par" />
                                                </xsl:call-template>
                                                dans le role de
                                                <xsl:value-of select="."/>
                                            </p>
                                        </xsl:for-each>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </xsl:for-each>


                    <div class="page-header" id="jury">
                        <h2>Jury du festival</h2>
                    </div>
                    <xsl:for-each select="/festival_cannes/jury/membre">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                            <h3 class="panel-title">
                                <xsl:call-template name="afficher_nom_artiste">
                                    <xsl:with-param name="artiste_id" select="@artiste" />
                                </xsl:call-template>
                            </h3>
                            </div>
                            <div class="panel-body">
                                <div class="row">
                                    <!-- details membre -->
                                </div>
                            </div>
                        </div>
                    </xsl:for-each>


                    <div class="page-header" id="palmares">
                        <h2>Palmares</h2>
                    </div>
                    <xsl:for-each select="/festival_cannes/palmares/prix">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title">
                                    <xsl:value-of select="@nom"/>
                                </h3>
                            </div>
                            <div class="panel-body">
                                <div class="row">
                                    <!-- condition artiste ou film -->
                                    <!-- details artiste ou film -->
                                </div>
                            </div>
                        </div>
                    </xsl:for-each>


                    <div class="page-header" id="artistes">
                        <h2>Liste des atistes</h2>
                    </div>
                    <xsl:for-each select="//artiste">
                        <div class="panel panel-default">
                            <div class="panel-heading">
                                <h3 class="panel-title">
                                    <xsl:value-of select="nom"/>
                                    &#160;
                                    <xsl:value-of select="prenom"/>
                                </h3>
                            </div>
                            <div class="panel-body">
                                <div class="row">
                                    <div class="col-md-4">
                                        <p>
                                            Sexe :
                                            <xsl:if test="@sexe != 'M'">
                                                Homme
                                            </xsl:if>
                                            <xsl:if test="@sexe != 'F'">
                                                Femme
                                            </xsl:if>
                                        </p>
                                    </div>
                                    <div class="col-md-4">
                                        <p>
                                            Nationalité :
                                            <xsl:call-template name="afficherPays">
                                                <xsl:with-param name="codePays" select="@pays" />
                                            </xsl:call-template>
                                        </p>
                                    </div>
                                    <xsl:if test="biographie">
                                        <div class="col-md-12">
                                            <p>Biographie :</p>
                                            <p>
                                                <xsl:value-of select="biographie"/>
                                            </p>
                                        </div>
                                    </xsl:if>
                                </div>
                            </div>
                        </div>
                    </xsl:for-each>
                </div>
                <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
                <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>
            </body>
        </html>
    </xsl:template>
    <!-- Afiichage nom artiste -->
    <xsl:template name="afficher_nom_artiste">
        <xsl:param name="artiste_id"/>
        <xsl:value-of select="//artiste[@id=$artiste_id]/nom" />
        <xsl:text> </xsl:text>
        <xsl:value-of select="//artiste[@id=$artiste_id]/prenom" />
    </xsl:template>

    <xsl:template name="afficherActeur">
        <xsl:param name="personnage"/>
        <a href="#{$personnage/@incarne_par}">
            <h4 title="Sexe&#160;:&#160;{//artiste[@id=$personnage/@incarne_par]/@sexe},&#160;Pays&#160;:&#160;{//nationalites/pays[@code=//artiste[@id=$personnage/@incarne_par]/@pays]}">
                <xsl:value-of select="//artiste[@id=$personnage/@incarne_par]/prenom" />
                <xsl:value-of select="//artiste[@id=$personnage/@incarne_par]/nom" />
            </h4>
        </a>
    </xsl:template>
    <!-- Affichage Pays -->
    <xsl:template name="afficherPays">
        <xsl:param name="codePays"/>
        <xsl:value-of select="//nationalites/pays[@code=$codePays]"/>
    </xsl:template>
</xsl:stylesheet>
