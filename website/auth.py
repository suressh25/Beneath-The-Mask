from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from . import db
import pyotp
import datetime
random_key=['KpVaSE3(od)C}32i2m(L', '{JavHxS2[}noxKwcY6C6', '}AZijBQnLSqBJLUuvBtQ', 'Pey(An6>PEpp65sE()e6', '(KDshDyfZ33}UGH)HF]H', 'gEnZJk)epj4tmHVz{Bb7', 'hMU]zSKXD9(qxyjeWH3t', 'xB7U4BXYeP3QBrAkNBbK', 'V(dvSLJzdGb4BDSWCbEn', 'QM[KP8dqBGi{3LqLspJC', '2(M58XK9>SntAcp[>M9H', 'NLnZ>AcPM({mc2UGo84Z', 'VT5KfR2[Qi5{)9[6SLRq', '(jP9{BoK7HkmTfh4J2[X', 'A6Zo4K4qRimGkvjQ2Hr7', 'rpyaMP]htJ(ybCz8k53h', 'WGDh}6RGZH8dAU4HJ79F', 'zZsPGe5}XLBtrNTPoUjd', ']Vkk}pKoWtU8sS544o4t', 'LAJ6DX}}Xotot>dCh2eC', '7}wWoqxruFXkjuS4C67S', 'X4vYRQ[MLSi)XXG[Wcxz', 'ggn6fX>Y)5vnE(>4TpB(', '{7Se9TTftc7>goieGbdn', 'vHSbQYoiEuCR3YD9>7Vr', 'CnqqbmdNNKyH7iojGWGj', 'rrCo53jrvQrTjbe6p7W8', ']fMLmC36ZyjjD8R23tMN', 'ijV2qHw9PmNkNuT2hFq4', 'VXnQeQ82E{ioYckb3YpA', 'mhLmK4CJZr3TR}DeY499', 'dnjsf5TzP6daeTio(wdd', 's3yDoV2]S{yUAzTuxeMW', 'afWV7S{fL>Q29PjMQ]oS', 'f7uYpELXzduF>DjgthzN', '5hnWSLXAW8PGKm{y6MU(', 'x}}]tmETeVx4aHyT6kwN', 'RSSr[PsRHgc>UmY>DL([', 'GxLZzjEC>imPerb9>qzA', '6yh8cz5U{vPEj8HZ(fjf', ']aMvyuyge23H6ERKhkQ4', '5>y8oh>>D>2kvhMbhQ(6', '(}v7zEB7Bzag{TDJE>M2', 'vGZc732X4Hgqnc]jhqzA', 'N]U]r6Y(Mmq3BCydA3az', 'hd64ATjrfTb}(vXTfB7L', 'A6u9s3dv>M9[jN{cm]kB', 'uM>TgVMGxji{j)T]j58]', '[NttqA[ddcV)s7RDcJz3', '64LFd[jupfXwC7fMNS[w', 'n}{{(VRVTt4f[f>HH99T', 'QRUCcff[]DE[k69YFzGk', '9XRRsCkfSZuLhq5yvr8>', 'skprGjS)TzZ{[(3N(rzq', 'mVc]LaMPqUAu4FqFu8R(', 'FKL7z}xQQE7VZF[)B7RK', 'vvdPQGpqWm}Yn(qpPbAR', 'UWEzxVSep6Q(c>[jpWF6', 'Mvv9rPxVkAbgQ8dmh[PZ', 'JPVwHwSfnjqyMXkAQvZQ', '5)qvKuaLRBk8KacumH3j', 'XrTgP]cZCNYzA8jcnJvR', '4NZN585oRKqpH26>L}zH', 'VU(2YyqpdKj5wgGyuSyW', 's3MeKzBFufkTkbmf}v8e', ']77tCaxpv[7QV46]WS6v', 'E5NB3DH]z6QZLEvHFnhR', 'BW6tr5pMPBy>i{mYhJcT', 'KUghVP2cFSV)S2{5CD(J', '5a}ApssLuPSLDham]A(w', 'a2M55sLvSM5ku96M{UJo', 'Db6X[uY9)EGcyFL[QPcM', ')d)AYTGs)aUF>vSQToCs', 'AAGtdy])arg>Hn9>XBLR', 'PYnVY3e6q}4R4hDdGJhA', 'kB4K7p483[uuL(j4iX)]', 'maoZYJ{wopbNA3jwrntq', 'y]X9JtCQkDkb8YTeX{5a', 'pw4]KWymPUwUC24]SXZq', '4m82KQ[odkVeHQxvZf]d', 'tmZd[(X>>ZXnD7orE5s9', 'S5RwDSHSRWdVzVVrYy[[', 'W>JFboPsqFB3}R}dvL{r', 'LfBH58P2m3ZLZ9{]kK3H', 'p>yeY)CefXxv])v2Qf(A', '{LVGx93sd9Y{QibTGod[', '4CdDJyA8N)Asw7M4EpMT', 'HFAJGX6QAoLi[z2gb3mu', '{WTHi2FDgLhAGteFBpwp', '5Lb[2fwpLe}WTtMzSXqr', 'C}aLFbDSmzvq]fmETXqh', 's4MPXYubCQ)kNdqLy(mB', 'pp5dFhoA7Lj7)[SiRrsY', 'Si7qHPSqV]M7kD7mdv36', 'yFrG]cAf9MiN{tsV}]{z', 'rWuXCC>SvBSWLQUwfi[)', '4)ZtX{2>NAgHC3oNtdmW', 'LbyQ]ehL(>Q2M{8BFCYi', 'opeL9msWap2DKja9)Nx[', '6dQcYPyo)pTVE327QA>L', 'aqPSm7)ioYGk{3XwpFVn', 'EJ98s7Dm[FjZx>YfpA>6', 'QF6P}rCYdEbKBA9Nyrx]', '{Fa)>FdTcwNgu9KNsi3b', 'CALJHG3ZkZXqAu6uwoPK', 'sWk6VmWDvfHnxt6HJExn', 'N(n4})E>[3J56gis3pGh', '4XrgytsUekTGBs]>9PFb', 'P3{nVxf57HPTKnW88FQj', 'bqbGjvj6pX5TxEZZjUNn', '9R]V2D2ZQv7C{ecACeE9', '(GKVNzqGSTXXoYqknnXj', 'g(W{jUmr[L}>fm2W6ano', 'dtMcUpQb9YRytzPimuEA', 'b}ZAx5i{5wvi3sV9bJiq', '5YXkpNpxodpUgqercAXz', 'ghpzZAAL2ZoXQ6}7Spzt', 'oVbZe[oeGbMqKo6FWcka', '3oWsXSSAYFC{58T6vRhE', 'c7>5VmXxv2fQdUTCuvJM', ')eNQDruSN42[Qxry>ggV', 'Tkt7d74PM(xzUrz7pM8S', 'bgNKaqP9ZXn}2WQQE{{X', 'pPVa7B]jBBn9hWhujP]s', 'ZF(4{oM3bupsAF>euf5M', 'pzzeMaFTmxuJxo{i2B]R', 'QKaB8XvyuPiKA2ZsQj]P', 'bW]Fk9vC[bSLLv8e}qB[', 'x6sLKMJ>m}YfhDgyPuAB', 'Q6G5p89Q])JGwU2r2A}H', 'aU9wyG565QswnXEJHGot', '2k8jC>XEgjuuV59FrvcR', 'JYCB5ZEwqDWFqxX4BM2f', 'pZXVVmq4fh}6PjkB9yBb', 'KeV9pA7(V6>TzRnVvumw', 'p5PctSXJBqFEwxSk5sL5', 'bNhfY(PQDfGZ)7PP69RV', 'Mw9Ewn)5{VP4HcVM2k}q', 'k6kh9CYXuM4[rqmnDU8T', '(HvzSdLMzC6tf9V9DJ9K', 'jH3A8>tu>9h3}ePgaiFB', '5z9sxz9nb6d(m5nuZeS5', 'GR89uiMVu9]v9(m>zG])', 'bgZ{9tSc8BiCM5U3JQqz', '8qQ>BFho}G3Ch)PBNr]H', 'jNS>)T2m{uLPbaoFu6ap', 'aToAwP7AMyV6dkuH4m}[', 'FMYgbrxT)5irqJEivaJw', 'dSY9kJuDsNgzsBQqmkF)', 'c9wGY3UeDdVR9Ld5qMfQ', '5i}s)RNGD{[3H[ZBfPUH', 'S]4qmA)Cuoegc8os(pcX', 'BYUrQ[5fGMJEU>Pon6kC', 'u)VHNZC(PwEaD8g)WqtB', 'pwfdDFoehwEeTNGmcdJ>', 'saq{K3{qW(5>3uryy)j]', 'w9FHyRemSDDZors7Fbs3', 'Mc>LUugQ)4PeH8uHBPm5', '6w4>TzNsShSFsRW85m7C', 'Zk6cJz4XHgZXDiH6XBRo', 'vm>uMM7ouwF7}RjbzcF7', '6k7>3Pj>pf(QA(ZV86ff', 'U4H>tFaQHR3(cmipufXV', ']L2JBGkTZWV)yST8HaU9', 'W{YAcfxY2hXyWDnvDhBG', '8aSgfdjwSPZPnuFHRojP', '8[cpGdj]VULNJoJSDytz', 'EA6vPmEBnE8hr2j)PWCa', 'Ub4ckt[RZh}2Xpi)449r', 'qy8AW3)A>o5WhQ3Uc)Fn', 'R7CEUqNzVZvgZKjiHFMj', 'RuEYDpX6TH6NtYbvZhQp', 's>)pMDNL7Y7LJrc8ZXzS', '[YKYSS4DYVN}4Ym8hcYw', 'j7a82YFAMFpMqPa7}hGx', '}2C{Y3Dfz3QSQ7FxBYok', 'XUJcnq5RY5{9nCv)CVL>', 'vsdu}y98gR7teYuaE4u3', '36edxJ2V]iWC9zhBRhSD', 'rBGJF9j5fVMfDzV5NLZ5', '54{xaXcLT)xqnuMkA6>x', 'c7PF82r>W]TbzUed(yRs', '>DUz5gDeVQ2EBq])69cf', 'ycY6aLV)BSkwtMmRKE3f', '7CMdSpVLaiRiCg}tPB[W', '3bFMgr{r7KFaq5Ue9zkp', 'tQRQuHWdAF)i4}[nn8fV', '9Kp3Ubv97Uj2u9p]4MWM', 'KowAWfjBweqfuAk(F[rY', 'AgL}WdQoLz>GjBVtoN]V', 'AfmT>NdwnNDWb(kHuK2m', ']8)S(]SmXAK6ehwPZgD8', 'fyzqmxqmknBpa6g{FXW>', '7jax7wex[d2hxwLVZdj4', 'wxjRQLU2]ZqCV4CG6}oh', 'E[Sawg2j2LdiUJqQr[bg', '}BgJtf6FYDo4FK7GwJQn', 'TKzdJWpCq5N9Fdagk>XM', 'ikNGXsca3Y(CeyP(Utkn', 'rTEuVjz2oheTs9R3RuCv', 'i3vuS8n6)VeFzgATBdoW', 'NfGRHSmWg6raPdHvvoJc', 'R8C4SQ2pxgXQKvW8iE2S', 'aL8NmRJiyWi5EP)q2w3j', 'w3fCgg(UgnrizhWiMVt]', '5Vtv(zBP8W46DyPHxgiG', '5UKM2F>U75EnC[vLYwho', 'W>DVupJckMr)u3t4X9rb', '2e5zMAF(}ScvHaZeyero', 'yKKaEsRH3hc9K>s[UxWL', 'TCoaLoX{CUXhu{vLByUf', 'z6o5q6H2NNF{d3JmBRpb', 'VqohdV4jxx2U>]]maoyt', 'E6tLfhLvPn2{ths6C{o5', 'kADUG)rxEorGNwJ)nwX]', ']xJm3RYvMHcQ6B2{a(Uq', 't2W3aD8>W}5Ad5rSdNNy', 'QJn{YT)KjckG>nbQhbsE', 'PKFTc{V62)CmCc{TU6Ky', 'Lr9yNHKD7tz3HbdDVS3a', 'QFnwUwpSJ4QTHHHkgf7z', 'NSQxkxyfBrto8NvnEH9g', 'edsejmsh{yRDVu)GuFri', 't)ACPuqW6CmFXHUZLMxX', 'uCC5xYZthry>nUo)Fvjr', 'bkbkAc9ffwuFH]gP7(KZ', 'XS)P8UpmCcvd]{pHCA43', 'kKtD(]mEQx]Jdk5M6x8V', '9}f5m4hPKFcZLToC7KoK', 'twvR{pzN5HbSiu32jNPT', 'nW>LJfkEdZ>{SYS9F8k}', 'RpSkGFwb(MksLnpcYhyj', '(t2UkUfUj8ic)ZSjKE]{', 'op]48fnE8a3(>b2G8EgB', 'u>tCeverZHaQjqLpMUgN', 'Fhgjsa3saibFdAfe]KuR', 'snahAFmD2pHj(N7Dy6SK', 'tWJzr](YEPHPLXc5WinL', '4JRrvBDZ>MN5Lx}R}Fjq', 'YiZ6vy6uaV}j)hdmCMz2', 'XupXhQYdGqR2K4MJmDKL', 'M2L>yjaGgB442mZ[x3y(', 'UpV>a5po6iksGfxZuG}9', 'hMKUNYTftLFz4VVuKy6Q', 'KNW}bmNJ3[7E9CPWbYDJ', 'Nd{bzQ8zcaN3gc6SL7gc', '}hLC>a5BF}6LUUg5y7Ev', 'AZiw2kjD4)BG6frr{6ae', 'dSJ5s7)KyGUPNbZLM6pv', 'vSzk34MCek8rQvDWE}{{', 'Y(h]77cW7[mfj7HZoWFx', 'Pm5fhaiRA2u[WGKN)]q5', '(cywmtZ8N2kY5Q3yFPR7', 'PzTx(y(iTSG2}rrHDj8z', '43vT4k8a>c]QD)5GmyG}', 'z5p(Lph}nPr2[C]CMAZV', '2WLzNW3cNbf)[yU[ZLGM', '>7WxmCCXnBxCwk6nFLPq', ')b9Qkb22kzjc4MiSf646', 'jMvJk)EQ{v7Yj>wQ5g4j', 'paqAF)bcnPb)ypMQzJ6W', '}(G[JKx5bM4V>kdLQxco', '5ijZU3zvBQ4o5V(UWxjT', 'U3WHayHZ5yErf6Go7idB', 'F7stNCvsW25Lq[k88Q5j', 'i(g94DGx6FjcT}fQygC4', 'NhWDQuGAFVMnu}6N])kC', '9psd(scEri8vS6BTPUZX', 'Cd4sYsvH6VpzvkGDFkZe', '9hHYu5dq)fWF5pn7tujL', 'dYL{avKPcqY[Z5pgHr9K', ')KGYDujozT>s6benS8Nd', 'g92ajFUz(KPmXRHVJNMM', 'm7jfkTBZnDKDcYFjP9M9', 'eQcoeyiQfBUptHC5gNXu', 'M[wbcfMxSA}VBixzBwuo', '}LUMM)kErGVi[hGsj6NG', '[dvKftnoiFDDSm3ddi9u', 'TddpQVYmxJejKxD(r2AP', 'ypccmz(HeM47T(zyEiZn', 'uo2x8fVR)mEWm2rmitDG', 's2qVvDnmK6pV4>xhqeuc', 'eqqeRtH8zvfgi8FB8[g2', 'Lr>dCedLgSWzfymZ9xWM', '5TBhmiPMAwrmv>JWibRh', '7xba8qyKTQQ9nig]Vd6i', 'ZHC)7q(jExM]bxiKm]}C', 'srhhnTWKy5KC6SicAKYW', 'EQbaWe9fg6x}}J)wPnW9', 'NNsGn(dJZJscZ[RtRSs(', 'hepWZyx9bukcgeVMsTte', 'Wf8Z7F7CJDgDLdK9wAoj', 'UCftTxk8)(q7yFMJgwag', 'tU9[CZbY}HbMgGAUFvBr', 'qJ[ZJTQZ({wSCGo56t8(', 'WaMFjbeK7hmGbSZFtYX9', '4r[{w7wepAxtChSi{x9U', 'v8a>AGMUu9ekT]TSe52y', '6EEYz2rBiNs6Yvhu({rG', 'KGThE)mDgBcXxL4biPcQ', ')tBZCk96ZeZN7ahj[tpp', 'Eyb7tDoHfEDeoVS2gKNu', 'q}wrj3>hZty>o32z5[az', 'ke}kHP5q{Stx(TogWiV}', 'q{VW3PQY4j4R]XynyCzv', 'qGFPCwFZVsSYXrifmzKV', 'C7y{RrLihHVK5(>bgYBq', 'UTAeu69ATAgC6nttGq[y', 'QYXR]AxW[5j9[uvmPkYs', '4BUTEZj22nnaSZtyMhUZ', '[wMmeLLNMm2>HNG(RS5Q', 'oR45{NZmXbVPFJssQmH9', 'cW87bchnR>nJ9wfiR(Hu', 'v7KVTKQvSoq[xAbq236>', 'jn]JiZ5FnhPEk2xwFsYy', 'hbkAmeibbhV9g{js5W5S', '(MWj>PTMzYWg2HDrFY[c', 'Wv]U5j)[(6LmJRjuFhzo', '8CfR}Q)W77HYAdbqk}cV', 'WrkNSsi9FKq{xXuxwZhX', 'L3cXn3P4we7TReMuFn>[', 'gik[PNX4YZzrPp78YXFu', '2CGdJeCdfdo]HF{{]4Hg', 'dpfRa}E(BgYKx6myN4Af', 'fD[M2F5ge)BLzbS4jNoT', 'ZFQkVEddM5uPcVhzZMYA', 'p]pZdzqpkGQWM}HmdQNo', 'k8LL2z5zN3VYczz9Rnpi', 'RkWQEUak}o]K7d[LJ6[j', 'wgiz>32pVGQNuNYP49dA', 'EE(ugUweSNTEpqyjY(6v', 'Mt}KxNpt5oJmWaKH4Rqf', 'AgMAx[5[PLK9AjBRqSoW', 'gPE(nV}LZBEz3Sn{fnEf', 'Ftnst8VLNaG]k64X6fkL', 'azFR2BLYA6wfo}DR6})X', 'HZ](Pv>Ffn4y)5C2fG]2', 'rWd7ujBN2xxKKpZtXJJr', 'SWXwcoviEn7gxqUivAgz', '8wxS}XU{Rw}W{Dwsf{J)', 'JzjU>}ryiGCEa5wkxreK', '3>Fs>CbtYZMw54AG85zw', 'gEpC[gTAQBJGwHjXRaQP', 'f[LaTj)3WPG](yQWryE5', ']VWJ(k{iNyiMwg7ij4jE', '}vzM8Su)HGzTPLwavMgp', 'dgLeH2cEzkkwtx45CGnL', '{caHB>(oDf3m[JWsuc(F', 'f2rBzXbFB(MjEvKr8M>>', '4tKTZ6}QUYFSh8XfxrmV', '}S{]q{wcXUvMMrDF6CJ}', 'cKDHrSCCubNv[JhKfpG}', 'jyMM6PUTVKexMA4)edjX', 'Yr)Cezg)Q}ZLyuGLTJhN', 'yTv)nF6kFLgw{fq[ExHo', 'kRqxG5Q)EQKb5yr>Ye>r', ']kobM[jBX5RmeiA5)u>A', '[hchzBUmz}u>Fdw6wFJ7', 'H6dN}UcP2PMKFwQMQAV3', 'dtbcF9G2WYv8HRPZWJbF', 'cx)fDP{RqdjC26o84w[u', 'WbbmgWvEWt[vCSJBRP[T', 'j47jgpxT9}X8X7i3Nc6[', 'sNi8niD)SPxgpHwDaP58', 'Us2x5LhaE}vg{k2hse}6', 'nLXwWL}5HNzyq3xNg>SH', 'qZAdm2YXX2hUevFrW2(3', 'f)yKPeAW[EU>D2Z[BmtG', '(7Q8CTSCnbyTwT}mkfv5', 'DRztbmkxTEFN7mgA(9wC', 'G2>FAeE4NK>}YF3R7BH[', 'fCcjVKCVw[6fFJdchRfX', 'r6(QRZK9zXPceXH7yPra', 'Z2C8SHicgA9[8yErX[pT', 'fKVx85YqmWqqyFEb6KqM', 'LgXXq]dHCrCU[NYfj{p6', 'Np7StSRjPHBNWENSofMi', 'EK8u2cL)dwFijPVdzoz3', 'bivsRSg>vJsRry)QaN8Q', '7ny]EdAsDQ42ppFD6(z)', 'CRoKLZ7s}xQq[UkR7HeN', 'denGQ[kPFBkpoQ46dJ72', 'jvUcR5jSH(GbeNZzZqBn', 'E[>wM3XvYxMsKT3UenBw', 'syv]ZiDuhUBbCvNEVF9{', 'SYP65gHq(kyhXqx3XKr7', '6jDS2[XvYcG5r>kADkQg', 'uBkmrRrMSVP{94)bGEPS', '4Fhmc8pgQjEaHz}84W5f', 'Xq3wq]JT9CKxv)gvJmwk', 'b6YJ}SmnCMAsmcXornsy', 'X(4pmnAYfEaJE8HMfFjS', 'De(NnoGkc4SEs7i2P2KQ', 'UUYZmQk9gi]M6RV5XMBz', 'Mw3bHHW3zQgwBx]QQUL[', 'j8npykhai2Ke6Nm}[H)E', 'YWp3Hh)mf4MU{gpkU5Gy', '5p]a>FxY>gj}gxB)q{W[', '6PQq]2q)24gYuqKq9Xsh', 'E>{)e[J2M]2vMBtYj58{', ']jKG2NKi6vc4kb]6nurs', 'XjCcsvP9KheGZtQhC{qt', 'Rp(ySM{]Gtfa22xMXF7F', 'ysR8Y{diTwoXSLVLMyD{', 'rNchJ]j8hu2kZsn3Zoi}', 'fka3MzfMFgf8fuNhBT>6', 'Q4i9wVUBCtE2deBL4[G}', 'YE}KM6}7M54}PxpL[7T9', 'A}VK5rYfPbdCALB6KVRd', '3YfGSD)GXWE6Qfvf7a{z', 'mHo5Fevv{csP[RHaKh>b', 'DBWXEDKC44>EoHzY7)gm', '(G2YopXh39i8(msoXGwx', 'df2b44bnfF4gLDZmkaZR', 'Zby5m76YuD]Kkq7cxJjw', '3XEsda9JbTa}PfeG>UWo', 'etwdM]TUxXPr99q]MFnG', 'Lt[]]{BQjH>fd3X)Z}rP', 'ibX6zCkZbNv>aUWbz[Jf', 'bBJ32zniLGQYV]aUzegh', 'ZCuG9s{[Q)B))]kvf}]P', 'b8BqMrEWmWZ)HFpo3uR6', 'CPQe9uZm4Dia>2JXhWdo', 'tE)2TYyC78YG9SkKZdSw', '}{Frax(FCQoZXueQBoDi', 'jkSQhDMyEP}FkYnpRrxx', 'JQ8ewLM>mZq(8[t2wvvL', 'V8BKLBYYgA2gHkNmc{W}', 'HqE]Ui8ntVVsu{R{(qo[', 'dqgb[kWZvx69iur6to>a', 'BQaY2r5Hco8kVN8Vt9rp', 'v2hAE}}N9uQ7[cz)TnWU', 'T7dyKDM)e(sA3UPaYPw)', 'x)Gs7aGNSbCB[RfLrQJd', 'UfGLyY6h68RoZFifTMKp', 'DLgjDaN3n>a8k{{3Aote', 'XyiAU384wLmM2wZybAsm', 'SofRgs6Ehkg3S)}[aJ9z', 'RYiP>C}pLLZz{gbbLC7m', '92QxH8xzMSLDa(KCqPSo', '6]4K9X7z(9YD>vwuS]xM', 'WxNSauZtH>h>mR5JF3]C', 'GW{pC>ZWxnTgF7jVBNWk', '3BD8Sv{c7SJNSAwDKRUR', '[Z7n64GPQZQAtnt6i66[', '59>rgUEcoJH3rrUB5]Tv', 'QsgU(Zk7LEWN97ABFHjT', 'Qew9)S)ACfzwo7VZsAuV', '7QFL{ts>MFgPmtr}Z8uo', '9LSfirAL(8)WSro)KJL]', '{GtEd7G(EsmNDgdmtKwK', 'ZgkeEHM))nAfPvXymz[K', 'pZJH}oagR>aCzQQD859J', 'rmQ)(LfipaAKKrKuv{kq', 'ZfZmcMeD>A[WS9nT9t]k', 'i9quCjK){NT5ojp]9p8z', 'e3]Juo]Z9NJ}Cn7FvEZx', 'ijW)HhtdT82]MBfx6N(Q', 'x]SS5iU[xdzN(gds(vPV', 'EfZXXm8fNZER686GDCzd', 'NhxypqxMvJHKdxd38dRo', '8fkBJUch]>G2S4UdpVc4', 'UwQk)Ba5NNBjQMU6pwqZ', '4{c[p(m2eMTvh9zGfMQm', '>UuTy2CQzbvqhzdn5agb', '5tuiphw(247[kd3FGfC[', 'o>jAsEPfY[wFCNb8n{aG', 'Z3EDGVWFFV8vhRp)e4z4', 'a2e}acjdpV2>yt]4h9S4', 'cZi9TsN6Cmx2G3]aTdJN', 'QUhBUDRpS{sgbXsVutQT', '}rKWN9B6(Lb}xGDc)HG7', '(bb6Sk7j7pbWdctHCXNT', 'RxjLMrhaPJFFdVHDdUN>', 'qa5vyoJk)NFKfd59nqkz', 'W6hrw[cecSM}NVNVN5F5', 'aue2(Q8XF>HsmV6>zKvw', 'SNhgSgvUjFu7fnwHERZg', 'wkZCqoH>L8qZWgGoHMwn', 'LEq9jfn)zvkC(tBzcP5N', '9pim)}gLuxxSxAMxtvtc', 'Y)h]MadRzW3KKdhXHaeq', '>mYPLc[J}o(>mTP{))8E', '4)PGbH8)mCKueWLhT)4B', 'Z[mpv4{h6NcHe>o4ftwf', '5z[]ey7rhvAv]bYJ2HRp', 'u])9mbYFuB2hA5pvbdoz', 'U5m>AT(>i4H3)ZUt[MMX', 'cEV}ED(Wv8B{(eLWLs7h', '>Dcq>(TZKEEiZ6v4f>yX', 'UyiE5jsZC9LjG6hsD49]', '42T]Jfu3{cT>buYJCFyk', 'XnzkmpXGzu5Kvq(wdH}U', ']9H8LQh2VhC4Pdq6yyk5', 'zQyX}9p5TBbrHb3ag7bk', 'W5WZQDUp[A>FJ2{NvUve', 'HYS{EGJt{X497d3UGiBD', 'SmHt}V}V)fxn4JixsvPn', 'GQemRiEFvoCkd2thW[T8', 'MjH8gbF5eL9yAEgF2)x(']
j = 0

auth = Blueprint("auth", __name__)


@auth.route("/login/", methods=["POST", "GET"])
@login_required
def login_page():
    if request.method == "POST":
        if request.form.get("username") == "bruh" and request.form.get("password") == "bruh@123":
            flash("password_correct", "success")
            current_user.ispassword = True
            db.session.commit()
            return redirect(url_for("auth.security"))
        return redirect(url_for("auth.login_page"))
    return render_template("login.html")


@auth.route("/security/", methods=["POST", "GET"])
@login_required
def security():
    if request.method == "POST":
        creds = {"Catname": "ALEX", "Hometown": "MADURAI", "Food": "PIZZA"}
        Catname = request.form.get("Catname")
        Hometown = request.form.get("Hometown")
        Food = request.form.get("Food")
        if Catname.upper() == creds["Catname"] and Hometown.upper() == creds["Hometown"] and Food.upper() == creds[
            "Food"]:
            flash("you have answered the security question correctly", "success")
            current_user.issecurityquestion = True
            db.session.commit()
            return redirect(url_for("auth.twofactor"))
        else:
            flash("Wrong Credentials", "danger")
            return redirect(url_for("auth.security"))
    if current_user.ispassword == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.login_page"))
    return render_template("login_security.html")


@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home_page"))


@auth.route("/last_page/")
@login_required
def last_page():
    global j
    if current_user.isofa == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.security"))
    a = random_key[j]
    j += 1
    return render_template("last_page.html",value=a)


@auth.route("/twofactor", methods=["POST", "GET"])
@login_required
def twofactor():
    if request.method == "POST":
        otp = int(request.form.get("otp"))
        if pyotp.TOTP("JBSWY3DPEHPK3PXP").verify(otp):
            current_user.isofa = True
            db.session.commit()
            flash("The TOTP 2FA token is valid", "success")
            current_user.completed=datetime.datetime.now()
            db.session.commit()
            return redirect(url_for("auth.last_page"))
        else:
            flash("You have supplied an invalid 2FA token!", "danger")
            return redirect(url_for("auth.twofactor"))
    if current_user.issecurityquestion == 0:
        flash("Not authorized", "danger")
        return redirect(url_for("auth.security"))
    return render_template("login_2fa.html")
