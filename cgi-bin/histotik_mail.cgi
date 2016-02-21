#!/usr/bin/perl
#
# Tik-111.361 Hypermediadokumentin laatiminen
# CGI-mail: Eritt�in yksinkertainen CGI/s�hk�posti-yhdysk�yt�v�
#
# (c) 1998-2000 Martti Rahkila
# Martti.Rahkila@tcm.hut.fi
#
# T�m� CGI-skripti on eritt�in yksinkertainen CGI/s�hk�posti-yhdysk�yt�v�,
# joka on tehty Teknillisen Korkeakoulun opintojaksoa Tik-111.361 Hyper-
# mediadokumentin laatiminen varten. Ohjelmaa saa vapaasti k�ytt�� ja
# muokata kurssin puitteissa. Ohjelmaa EI saa (eik� kannata) k�ytt�� muihin tarkoituksiin.
# Martti Rahkila ei vastaa mink��nlaisista vahingoista, mit� t�m�n ohjelman
# k�ytt� voi aiheuttaa.
#
# http://www.tcm.hut.fi/hype/
#
# v0.0 19.01.1998
# v1.0 21.01.1998
# v1.1 23.03.1999
# v1.2 24.05.1999
# v1.21 21.02.2000
#
# Seuraavia asioita kannattaa pohtia:
# - miten t�t� ohjelmaa voisi parantaa?
# - l�yd�tk� bugeja tai turvallisuusriskej�?

### Konfigurointi:

# sendmail-ohjelman sijainti ja kutsu (kts. man sendmail):
$sendmail = "/usr/lib/sendmail -t -oi";
# mieti seuraavia m��rittelyj�
$toaddress = "pj\@niksula.hut.fi";
#defaults
$subject = "histo.tik Palaute";
$server = "hype.tcm.hut.fi";
$nexturl = "../Anna_palautetta/kiitos.html";

### P��ohjelma

if (&LueData) {
    &LahetaMeili;
} else {
    &Virhe('Lomake on virheellinen');
}

exit(0);

### Aliohjelmat:

## &LueData: lukee lomakkeelta saadun sy�tteen ja palauttaa sen
## assosiatiivisena taulukkona tai arvon false, jos sy�tett� ei
## ole

sub LueData {
  local (*input) = @_ if @_;
  local ($method, $i, $key, $val);

# mill� metodilla ohjelmaa on kutsuttu
  $method = $ENV{'REQUEST_METHOD'};
# luetaan sy�te
  if ($method eq "GET") {
      $input = $ENV{'QUERY_STRING'};
  } 
  elsif ($method eq "POST") {
    read(STDIN,$input,$ENV{'CONTENT_LENGTH'});
  }

# separoidaan muuttujat
  @input = split(/[&;]/,$input); 

# url-dekoodataan sy�te
  foreach $i (0 .. $#input) {

# +-merkki vastaa v�lily�nti�
    $input[$i] =~ s/\+/ /g;

# erotellaan muuttujan nimi ja arvo
    ($key, $val) = split(/=/,$input[$i],2);

# muunnetaan erikoismerkit heksamuodosta
    $key =~ s/%(..)/pack("c",hex($1))/ge;
    $val =~ s/%(..)/pack("c",hex($1))/ge;

# assosioidaan muuttujan nimi ja arvo
# \0 erottaa useammat arvot
    $input{$key} .= "\0" if (defined($input{$key})); 
    $input{$key} .= $val;

  } #foreach

  return scalar(@input); 
}

## &Virhe(): Antaa virheilmoituksen ja keskeytt�� ohjelman suorituksen

sub Virhe {
    local($message) = @_;

    print "Content-type: text/html\n\n";
    print <<EOF
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<HTML>
  <HEAD>
    <TITLE>histo.tik</TITLE>
    <LINK rel="stylesheet" type="text/css" href="../histotik.css" title="histo.tik">
  </HEAD>
  <BODY bgcolor="#000000" text="#000000" link="#003366" alink="#3399FF" vlink="#3366CC">
    <CENTER>
      <TABLE background="../Images/background.gif" width="700" border="0" cellspacing="0" cellpadding="0">
        <TR>
	  <TD><IMG src="../Images/vy-kulma.gif" alt="" width="50" height="50"></TD>
	  <TD width="600" height="50"><IMG src="../Images/blank.gif" alt=""></TD>
	  <TD><IMG src="../Images/oy-kulma.gif" alt="" width="50" height="50"></TD>
	</TR>
	<TR>
	  <TD><IMG src="../Images/blank.gif" alt=""></TD>
	  <TD class="perus">
	    <H1>$message</H1>
	    Palaa t&auml;st&auml; <A href=\"../Anna_palautetta/anna_palautetta.html"\>edelliselle sivulle.</A>
	  </TD>
	  <TD><IMG src="../Images/blank.gif" alt=""></TD>
	</TR>
	<TR>
	  <TD><IMG src="../Images/va-kulma.gif" alt="" width="50" height="50"></TD>
	  <TD width="600" height="50"><IMG src="../Images/blank.gif" alt=""></TD>
	  <TD><IMG src="../Images/oa-kulma.gif" alt="" width="50" height="50"></TD>
	</TR>
      </TABLE>
      <P>
      <TABLE background="../Images/background.gif" width="700" border="0" cellspacing="0" cellpadding="0">
        <TR>
	  <TD><IMG src="../Images/vy-kulma.gif" alt="" width="50" height="50"></TD>
	  <TD width="600" height="50"><IMG src="../Images/blank.gif" alt=""></TD>  
	  <TD><IMG src="../Images/oy-kulma.gif" alt="" width="50" height="50"></TD>
	</TR>
	<TR>
	  <TD><IMG src="../Images/blank.gif" alt=""></TD>
	  <TD class="keskitetty" align="center">[<A href="../Vuosi_vuodelta/alkutaival.html">Vuosi&nbsp;vuodelta</A>] [<A href="../Alkorytmi/alkorytmi.html">Alkorytmi</A>] [<A href="../Lenskin_Dynamo/lenskin_dynamo.html">Lenskin&nbsp;Dynamo</A>] [<A href="../Slangia_ilmioita/slangia_ilmioita.html">Slangia&nbsp;&&nbsp;ilmi&ouml;it&auml;</A>] [<A href="../Kilta_numeroina/kilta_numeroina.html">Kilta&nbsp;numeroina</A>] [<A href="../Kuva-arkisto/kuva-arkisto.html">Kuva-arkisto</A>] [<A href="../Syyllisia_selityksia/syyllisia_selityksia.html">Syyllisi&auml;&nbsp;&&nbsp;selityksi&auml;</A>] [<A href="../Anna_palautetta/anna_palautetta.html">Anna&nbsp;palautetta</A>]</TD>
	  <TD><IMG src="../Images/blank.gif" alt=""></TD>
	</TR>
	<TR>
	  <TD><IMG src="../Images/va-kulma.gif" alt="" width="50" height="50"></TD>
	  <TD width="600" height="50"><IMG src="../Images/blank.gif" alt=""></TD>
	  <TD><IMG src="../Images/oa-kulma.gif" alt="" width="50" height="50"></TD>
	</TR>
      </TABLE>
    </CENTER>
  </BODY>
</HTML>
EOF
    ;
    exit(1);
}

## &LahetaMeili: L�hett�� viestin sy�tteess� annettuun osoitteeseen
## sendmail-ohjelmalla

sub LahetaMeili {
    local(*input) = @_ if @_;
    local($key,$val);

# luetaan sy�tteest� tarvittavat arvot
    foreach $key (keys %input) {
	$fromname = $input{'nimi'},next if ($key eq "nimi");
	$fromaddress = $input{'sposti'},next if ($key eq "sposti");
	$subject  = $input{'otsikko'},next if ($key eq "otsikko");
	$data = $data . "$key:\t$input{$key}\n";
	next;
    }

# varmistetaan, ett� riitt�v�sti tietoja on annettu
    unless ($fromaddress =~ /^.+\@.+/) { &Virhe('L�hett�j�n osoite on virheellinen');}
    unless ($fromname) { &Virhe('L�hett�j�n nimi puuttuu')}

# filtter�id��np�s v�h�n inputtia, mieti miksi!
    $fromname =~ tr/[\n\r\;\0]//d;
    $fromaddress =~ tr/[\n\r\;\0]//d;
    $fromname = substr($fromname,0,100);
    $fromaddress = substr($fromaddress,0,100);
    $subject =~ tr/[\n\r\0]//d;
    $subject = substr($subject,0,100);

# kutsutaan sendmail-ohjelmaa
    open(MAIL,"| $sendmail") || 
	&Virhe('sendmail-ohjelman kutsu ei onnistunut');

# L�hetet��n data
    print MAIL <<EOF;
From: $fromname <$fromaddress>
To: $toaddress
Subject: $subject
X-Mail-Gateway: Hype CGI-mail

$data
EOF
    ;
    close(MAIL);

# palautetaan url
    print "Location: $nexturl\n\n";
}



