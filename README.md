# Gymnasiearbete 24/25

 Axel Lampa

**Denna README.md är till för mig att få en grundläggande men lite mer detaljerad bild av arbetet, vilket underlättar sammanställningen nästa termin. Detta ska bara vara en slags tillfällig dokumentation för mig att skriva ner idéer & utförande som jag vill ha med i den riktiga dokumentationen. Därmed kommer valda rubriker tas för att skriva ner undersökning.**

## Syfte

Detta examensarbete undersöker _[fångarnas dilemma]_, det vanligaste problemet man stöter på inom spelteori som ofta används för att analysera och få rationella lösningar i konflikter. Problemet går ut på att två individer måste fatta beslut utan att känna till den andres val. Beroende på deras val kan de antingen samarbeta eller agera själviskt, vilket kommer påverka deras resultat. Genom att replikera och simulera Fångarnas dilemma i Visual Studio Code med Python, syftar examensarbetet till att ge en djupare förståelse för de strategier och tankesätt som används för att få det bästa resultatet.

Ett särskilt fokus ligger på att replikera och analysera Robert Axelrods iteration av _[fångarnas dilemma]_, även känd som _Axelrod’s Tournament_, som publicerades i hans verk _[The Evolution of Cooperation]_. Axelrods forskning visar hur samarbete kan uppstå bland konflikter, och detta examensarbete syftar till att replikera, undersöka och validera hans slutsatser genom flera simuleringar.

Den vanligaste versionen av dilemmat kan visualiseras som följande:

|  | **Fånge B är tyst** | **Fånge B vittnar** |
| ------------- | ------------- |---------------|
| **Fånge A är tyst** | Båda får 1 år | A får 5 år, B friges |
| **Fånge A vittnar** | A friges, B får 5 år | Båda får 3 år |

## Teori

### Probabilistisk strategi

Låt straffet man får vara poäng istället. Detta förenklar att förstå samband och sannolikhet. För en djupare bild brukar man rita upp dilemmat som följande:

|  | **Fånge B är tyst** | **Fånge B vittnar** |
| ------------- | ------------- |---------------|
| **Fånge A är tyst** | $(R, R)$ | $(S, T)$ |
| **Fånge A vittnar** | $(T, S)$ | $(P, P)$ |

där

- $R$ (Reward) är resultatet om båda är tyst
- $T$ (Temptation) är resultatet för att vittna när den andra är tyst
- $S$ (Sucker) är resultatet för att vara tyst medan den andra vittnar
- $P$ (Punishment) är resultatet om båda vittnar

och låt

- $R = 3$
- $T = 5$
- $S = 0$
- $P = 1$

Då får vi denna ojämlikhet: $T$ > $R$ > $P$ > $S$

Anta att båda fångar får slumpmässigt välja sin strategi.

- Låt $x$ vara sannolikheten att fånge A är tyst. Då kan $(1-x)$ vara sannolikheten att fånge A agerar för sitt eget bästa, alltså vittnar.
- Låt $y$ vara sannolikheten att fånge B är tyst. Då kan $(1-y)$ vara sannolikheten att fånge B agerar för sitt eget bästa, alltså vittnar.

Alla möjliga utfall för A kan beräknas utifrån payoff matrisen. Det går som följande:

- Båda är tyst. Detta kan ske med sannolikheten $xy$. Båda fångarna får $R$ som resultat.
- Fånge A är tyst, fånge B vittnar. Detta kan ske med sannolikheten $x(1-y)$. Fånge A får $S$ som resultat.
- Fånge A vittnar, fånge B är tyst. Detta kan ske med sannolikheten $(1-x)y$. Fånge A får $T$ som resultat.
- Båda vittnar. Detta kan ske med sannolikheten $(1-x)(1-y)$. Fånge A får $P$ som resultat.

Förväntade utfall för A blir då summan av allt vilket blir:

$Utfall_A(x, y) = Rxy + Sx(1-y) + Ty(1-x) + P(1-x)(1-y)$

Förenklat så blir detta följande:

$Utfall_A(x, y) = 3xy + 0x(1-y) + 5y(1-x) + 1(1-x)(1-y)$ \
$Utfall_A(x, y) = 3xy + 5y(1-x) + 1(1-x)(1-y)$

För att fortsätta expanderar vi termerna:

$Utfall_A(x, y) = 3xy + 5y-5xy + 1-y-x+xy$

Vilket till sist blir:

$Utfall_A(x, y) = -xy + 4y + 1 - x$

Samma teori gäller för fånge B:

$Utfall_B(x, y) = Rxy + Tx(1-y) + Sy(1-x) + P(1-x)(1-y)$

Däremot så blir den andra och tredje termens koefficient för resultat omvänt eftersom när fånge A vittnar och fånge B håller tyst så får fånge B $S$ och inte $T$. Förenklingar leder till följande:

$Utfall_B(x, y) = Rxy + Tx(1-y) + Sy(1-x) + P(1-x)(1-y)$ \
$Utfall_B(x, y) = 3xy + 5x(1-y) + 0y(1-x) + 1(1-x)(1-y)$ \
$Utfall_B(x, y) = 3xy + 5x −5xy + 1 − y −x + xy$ \
$Utfall_B(x, y) = -xy + 4x + 1 - y$

Nu kan vi kombinera $Utfall_A(x, y)$ och $Utfall_B(x, y)$ för att få ett enat perspektiv:

$Utfall(x, y) = (-xy+4y+1-x) + (xy+4x+1−y)$ \
$Utfall(x, y) = -2xy + 3x + 3y + 2$

## Programmering

Se till att NumPy och Matplotlib Pyplot är installerade. Detta kan göras som följande i en terminal:

``` bat

python -m pip install numpy
pip install matplotlib

```

Kod för isaritm av individuella utfall.

``` python

import numpy as np
import matplotlib.pyplot as plt

# resolution
x = np.linspace(0, 1, 500)  # More points for better detail
y = np.linspace(0, 1, 500)  # More points for better detail

# meshgrid for the plot
X, Y = np.meshgrid(x, y)

def payoff_function(X, Y):
    return -X * Y + 4 * Y + 1 - X


Z = payoff_function(X, Y)

plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 50), cmap='YlOrRd')

# contour lines for equilibrium
contour_lines = plt.contour(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 16), colors='black', linewidths=0.3)

colorbar = plt.colorbar(contour, label='Payoff')
colorbar.set_ticks(np.arange(int(Z.min()), int(Z.max()) + 1))

# Labels and title
plt.title('Payoff Contour Plot for Prisoner A')
plt.xlabel('Probability of Player A Cooperating (x)')
plt.ylabel('Probability of Player B Cooperating (y)')


plt.show()

```

Kod för isaritm av sammanlagda utfall:

``` python

import numpy as np
import matplotlib.pyplot as plt

# resolution
x = np.linspace(0, 1, 500)  # More points for better detail
y = np.linspace(0, 1, 500)  # More points for better detail

# meshgrid for the plot
X, Y = np.meshgrid(x, y)

def payoff_function(X, Y):
    return -2 * X * Y + 5 * X + 5 * Y + 2


Z = payoff_function(X, Y)

plt.figure(figsize=(8, 6))
contour = plt.contourf(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 50), cmap='YlOrRd')

# contour lines for equilibrium
contour_lines = plt.contour(X, Y, Z, levels=np.linspace(Z.min(), Z.max(), 16), colors='black', linewidths=0.3)

colorbar = plt.colorbar(contour, label='Payoff')
colorbar.set_ticks(np.arange(int(Z.min()), int(Z.max()) + 1))

# Labels and title
plt.title('Payoff Contour Plot for Prisoner\'s Dilemma')
plt.xlabel('Probability of Player A Cooperating (x)')
plt.ylabel('Probability of Player B Cooperating (y)')


plt.show()

```

## Länkar

- [Loggbok/Backlog]
- [Repository]

## Källor som kommer användas under arbetets gång

- [Prisoners Dilemma - Wikipedia](https://en.wikipedia.org/wiki/Prisoner%27s_dilemma)
- [Axelrods Tournament](https://cs.stanford.edu/people/eroberts/courses/soco/projects/1998-99/game-theory/axelrod.html)
- [Tournaments — Axelrod 0.0.1 documentation](https://axelrod.readthedocs.io/en/fix-documentation/reference/overview_of_strategies.html)
- [The Evolution of Cooperation*](https://ee.stanford.edu/~hellman/Breakthrough/book/pdfs/axelrod.pdf)
- [Nashpy documentation](https://nashpy.readthedocs.io/en/latest/index.html)
- [The Prisoner’s Dilemma: A Mathematical Analysis](https://www.horacemann.org/uploaded/HoraceMann/Images/News/2011-2012_News/James_Ruben_--_original.pdf)

[Loggbok/Backlog]: https://docs.google.com/document/d/1yisuDjvD-EE_7QIu7x1w64V1gVMFPEqq9ytYGSEC3EA/edit
[Repository]: https://github.com/axellampp/Gymnasiearbete---Axel
[Fångarnas dilemma]: https://en.wikipedia.org/wiki/Prisoner%27s_dilemma
[The Evolution of Cooperation]: https://ee.stanford.edu/~hellman/Breakthrough/book/pdfs/axelrod.pdf
