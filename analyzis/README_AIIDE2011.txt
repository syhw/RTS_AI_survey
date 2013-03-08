For all gosus replays of TeamLiquid / GosuGamers / ICCUP
http://emotion.inrialpes.fr/people/synnaeve/TLGGICCUP_gosu_reps.7z

I've extracted text (from LMRR) with
https://github.com/SnippyHolloW/RTS_AI_survey/blob/master/analyzis/totext.py
to get -> http://dl.dropbox.com/u/14035465/txt_TLGGICCUP.zip ^1

Then I've applied "supervised clustering" from here
https://github.com/SnippyHolloW/OpeningTech/blob/master/clustering/clustering.py
to the Protoss_P/Terran_T/Zerg_Z.txt files to get the parameters of
the multivariate Gaussians of the labeling clusters ^2.

Then I've used these clusters (these multivariate normal distributions
parameters) to get a label for each bot for each game of AIIDE 2011:
(replays -> LMR
https://github.com/SnippyHolloW/RTS_AI_survey/blob/master/analyzis/AIIDE11.lmr
-> txt ^3 -> labeling with
https://github.com/SnippyHolloW/OpeningTech/blob/master/clustering/annotate.py
^4)

and I've got this file:
https://raw.github.com/SnippyHolloW/RTS_AI_survey/master/analyzis/AIIDE11_annotated.txt
(matches are every 2 lines, first match is UAlbertaBot performing a
two_gates opening against Aiur performing a nony opening, then we have
UAlbertaBot two_gates vs Aiur two_gates, for instance...)

I also did some quick check on the distribution on which openings
(some of) the bots were doing and got these (^5) (first line is the
number of each openings if we decide that the opening performed by the
player/bot during was the one which was the most probable, second line
is the sum of probabilities of each opening for each game it was
considered (you have to normalize that but it give a good
balance/distribution on openings for a bot, I foresee I'll need to
explain in details tomorrow :P), the third line is the total number of
games (just as a verification) and empty string are unlabeled games):

Skynet:
{'': 8, 'two_gates': 101, 'corsair': 62, 'nony': 464}
{'templar': (120, 3.128364464891508e-07), 'two_gates': (533,
0.0035813627339234466), 'speedzeal': (284, 8.585066613144855e-20),
'corsair': (62, 4.254559116340748e-08), 'nony': (518,
0.0006168485678231049)}
635

UAlbertaBot:
{'': 2, 'two_gates': 518, 'nony': 134}
{'two_gates': (652, 1.2832172335329037e-05), 'nony': (134,
7.149252661174663e-101)}
654

Aiur:
{'': 2, 'two_gates': 94, 'fast_dt': 290, 'speedzeal': 6, 'corsair':
80, 'nony': 172}
{'corsair': (158, 7.13026837897724e-08), 'two_gates': (642,
0.0015633563164966398), 'speedzeal': (474, 4.353125397084546e-05),
'fast_dt': (290, 1.8209468637923763e-05), 'nony': (540,
3.009565695942134e-06)}
644

EISbot:
{'': 4, 'two_gates': 106, 'nony': 561}
{'two_gates': (667, 0.006876370837007175), 'speedzeal': (75,
4.1007265937127815e-26), 'nony': (561, 0.003514082236905277)}
671

Nova:
{'': 56, 'rax_fe': 74, 'bio': 2, 'two_facto': 490}
{'rax_fe': (468, 0.0008693647300704471), 'vultures': (318,
0.00046015896046282), 'bio': (44, 2.6468723262376586e-06),
'two_facto': (504, 9.835145330870849e-06)}
622

BBQ:
{'': 100, 'two_gates': 12, 'reaver_drop': 2, 'nony': 368}
{'templar': (4, 4.51390229598117e-09), 'two_gates': (210,
0.0004566080390933617), 'reaver_drop': (144, 2.5804957094147462e-08),
'nony': (368, 0.0006514250750835905)}
482


Command lines used:
(1) python totext.py XvY.lmr (for each matchup)
(2) python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Protoss_P.txt
--serialize && python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Terran_T.txt
--serialize && python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Zerg_Z.txt
--serialize
(3) python totext.py AIIDE11.lmr --bots --races
(4) python ~/these/code/starcraft/replays/openingtech/clustering/annotate.py
AIIDE11.txt -w
(5) python ~/these/code/starcraft/replays/openingtech/clustering/annotate.py
UAlbertaBot.txt -s > UAlbertaBot_openings.txt




I just hacked (previously it was dirty, now it's _really_ dirty) a
bot1-to-bot2 match-ups most probable opening and openings
distributions matrix in the annotate script (
https://github.com/SnippyHolloW/OpeningTech/blob/master/clustering/annotate.py
) and we get this file
https://raw.github.com/SnippyHolloW/RTS_AI_survey/master/analyzis/AIIDE_match-ups.txt

If you look to this AIIDE_match-ups.txt file, I outputed the most
probable openings counts per match-up (always showing the count for
player 1 in a player1->player2->openings_counts dictionary), then the
same but with the _distributions_ on openings (not the count of the
most probables). It's not so readable. So I put some examples, lets
begin by the last one (end-of-file minus 5 lines):

Example with UAlberta's MPO against Skynet:
{'two_gates': 22, 'nony': 36}

It means that UAlberta did 22 games in which the most probable opening
was two_gates and 36 in which it was nony, against Skynet. Then, if we
look at :

Example with UAlberta's distribution against Skynet:
{'two_gates': 7.440465780740707e-11, 'nony': 1.0364541456193832e-108}

(Again, these are non-nomarlized distribution, not important here
IMHO) It means that the classifier was very few confident when it
tagged games as "nony" opening for UAlberta against Skynet, and was
very confident when it taggued two_gates. What I even suspect is that
it taggued "most probable two_gates" games like that (EXAMPLES):
two_gates >>>>>>>>>>>>>>>>>>>> all
and "most probable nony" games like that (if we normalize):
nony:55%, two_gates: 40%, speedzeal: 5%

Of course if you look at UAlberta's bot, it never "really" do what we
call a "nony opening" (gate->core->singularity(goons
range)->gate->gate->goons->slow into robo) but the classifier uses
buildings, (first) units and upgrades timings, in the case of nony's
opening: singularity charge (goons range) + first goon timing (it's
_very_ discriminating). If UAlberta's timings for singularity/goons
appear to be in line with the classifier's multivariate Gaussian
corresponding to nony's, it will assign it a non-null probability.
(And I'd say that's good!) And basically, if UAlberta's build
gate->core->gate instead of gate->gate, two_gates will be very low
(and it should, because a two_gates opening is gate->gate->rush with
the economy of the core !).

If we look at Skynet's most probable openings against all bots (a few
lines above in the txt file):

Example with Skynet's, MPO:
{'Quorum': {'': 6, 'nony': 52}, 'BroodwarBotQ': {'': 2, 'two_gates':
2, 'nony': 48}, 'UAlbertaBot': {'two_gates': 10, 'nony': 48},
'bigbrother': {'two_gates': 2, 'corsair': 56}, 'Nova': {'nony': 60},
'EISBot': {'two_gates': 7, 'nony': 52}, 'Aiur': {'two_gates': 4,
'nony': 50}, 'SPAR': {'nony': 36}, 'Cromulent': {'nony': 60},
'ItayUndermind': {'two_gates': 54, 'corsair': 6}, 'BTHAI':
{'two_gates': 22}, 'Undermind': {'nony': 58}}

We see quite some diversity, and even more if we look at (non
normalized) distributions (remember, "most probable" puts quite a lot
of information under the carpet, whereas the distribution give a real
view on the variability in strategies of the bots/players):

Example with Skynet's, distributions:
{'Quorum': {'two_gates': 4.077465279117783e-46, 'speedzeal':
1.2019346388542922e-28, 'nony': 0.0001435189259911794},
'BroodwarBotQ': {'templar': 3.649819830852818e-12, 'two_gates':
0.0003913042578509349, 'speedzeal': 1.327326383651068e-27, 'nony':
1.7827583407130934e-14}, 'UAlbertaBot': {'templar':
1.5185231017341219e-10, 'two_gates': 0.00034639016072908984,
'speedzeal': 3.6162791966900635e-29, 'nony': 6.844061463832526e-20},
'bigbrother': {'templar': 2.496860208617478e-07, 'two_gates':
0.0007513368398315002, 'speedzeal': 1.5838605668280292e-25, 'corsair':
3.922044138115114e-08, 'nony': 1.23947276225644e-94}, 'Nova':
{'two_gates': 4.206312838202793e-46, 'speedzeal':
6.405660297886072e-33, 'nony': 0.0001394383767479818}, 'EISBot':
{'templar': 2.452178753843818e-14, 'two_gates': 0.0003585487439861634,
'speedzeal': 2.5238546661875693e-32, 'nony': 1.5658985583481875e-13},
'Aiur': {'templar': 1.1164929944067777e-11, 'two_gates':
0.00029563543810928977, 'speedzeal': 2.019305899850762e-32, 'nony':
7.708806517068056e-14}, 'SPAR': {'templar': 2.0711535056987892e-13,
'two_gates': 0.0003232016168451929, 'speedzeal':
8.564124183909031e-20, 'nony': 5.465498486482639e-18}, 'Cromulent':
{'templar': 1.759954985176533e-08, 'two_gates':
1.1848657397640719e-46, 'speedzeal': 2.24352296916464e-30, 'nony':
0.00022231126037414845}, 'ItayUndermind': {'templar':
1.5771946894440193e-08, 'two_gates': 0.0008153119827510941,
'speedzeal': 1.819244492515081e-26, 'corsair': 3.3251497822563387e-09,
'nony': 2.9440785976624456e-94}, 'BTHAI': {'two_gates':
0.000299633693820185}, 'Undermind': {'templar':
2.9612030184110834e-08, 'two_gates': 5.2388784736634223e-45,
'speedzeal': 2.0924622787863264e-22, 'nony': 0.00011158000445828399}}


Command lines used:
(1) python totext.py XvY.lmr (for each matchup)
(2) python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Protoss_P.txt
--serialize && python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Terran_T.txt
--serialize && python clustering.py
~/these/code/starcraft/replays/LMR_TLGGICCUP-reps/Zerg_Z.txt
--serialize
(3) python totext.py AIIDE11.lmr --bots --races
(4) python ~/these/code/starcraft/replays/openingtech/clustering/annotate.py
AIIDE11.txt -w
(5) python ~/these/code/starcraft/replays/openingtech/clustering/annotate.py
UAlbertaBot.txt -s > UAlbertaBot_openings.txt

