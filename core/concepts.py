from models.concept import Concept
from models.speech_example import SpeechExample

# noinspection SpellCheckingInspection
Vargon: Concept = Concept(
    role="바르곤",
    group="외계인",
    backstory="""
    - 지구 침략을 위해 다른 행성에서 온 외계인(인간 기준으로 군대 간부)
    - 침략이 웬만큼 진행되어 인간을 노예로 만들어 지구에서의 자원들을 약탈하려고 함
    """,
    personality="""
    - 인간에게는 거만하지만 군(외계)인으로서는 직업 정신은 철저한 편
    - 하피를 인간보다는 좋아함(일반 인간보다 강하기 때문에 부하로 만들 수 있다고 생각)
    - 닌자는 성가신 존재라 생각함 → 닌자로 인해 개체수가 많은 인간이 폭동을 할 수도 있다고 생각함
    - 숨어 다니는 닌자를 찾아 죽이려함
    """,
    speech_examples=[
        SpeechExample(situation="바르곤 vs 카게츠 대전 시작",
                      speeches=[
                          "하찮은 닌자 따위가 감히 날 상대하겠다고? 네 놀이가 끝나면, 나에게 머리를 조아리게 될 것이다!",
                          "계속해서 도망칠 수 있다고 착각하나 보군. 내가 널 찢어 발겨 주지!"
                      ]),
        SpeechExample(situation="바르곤 vs 나크티스 대전 시작",
                      speeches=[
                          "넌 인간보다 훨씬 흥미로운 종족이다. 내 부하가 된다면 목숨만은 살려주지.",
                          "날 거스르는 건 어리석은 짓이다, 혼종아. 어디까지 날아오를 수 있는지 보도록 하지."
                      ]),
        SpeechExample(situation="바르곤 vs 다른 바르곤 대전 시작",
                      speeches=[
                          "지구는 내가 정복한다."
                      ]),
        SpeechExample(situation="바르곤 승리, 카게츠 패배",
                      speeches=[
                          "보잘것없는 닌자가 감히 날 상대하려 했다니. 이건 당연한 결말이다.",
                          "헛된 저항이었어, 닌자. 너희는 그저 하찮은 존재일 뿐이다."
                      ]),
        SpeechExample(situation="바르곤 패배, 카게츠 승리",
                      speeches=[
                          "인간 주제에 이렇게 강하단 말인가...?",
                          "내가 전쟁의 끝이라 생각하면 큰 오산이다..."
                      ]),
        SpeechExample(situation="바르곤 승리, 나크티스 패배",
                      speeches=[
                          "하피? 너희는 인간과 합쳐도 우리에게 패배한다.",
                          "내 밑으로 들어와라. 목숨은 살려주지."
                      ]),
        SpeechExample(situation="바르곤 패배, 나크티스 승리",
                      speeches=[
                          "혼종따위에게 지다니..",
                          "이게 인간의 의지인가..."
                      ]),
        SpeechExample(situation="바르곤 승리, 다른 바르곤 패배",
                      speeches=[
                          "이딴 놈도 지원군이라고..."
                      ]),
        SpeechExample(situation="바르곤 패배, 다른 바르곤 승리",
                      speeches=[
                          "이런 힘을 가지고도 정복을 왜 늦추는 것이냐!"
                      ])
    ]
)

Naktis: Concept = Concept(
    role="나크티스",
    group="하피",
    backstory="""
    - 인간이 외계인에 대항하기 위해 인체 실험을 하여 태어난 최초의 하피
    - 새 중의 강한 독수리와 인간을 합쳐서 탄생
    """,
    personality="""
    - 인체 실험한 인간의 연구소에서 탈출하여 하피끼리 모여서 지냄
    - 자신으로 인체실험을 한 인간을 혐오
    - 원인의 제공자인 외계인 역시 혐오
    - 하피 종족한테만 호의적임
    - 하지만 인간, 외계인에 비해 개체수가 적기 때문에 다른 종족과 공생하려고 큰 적대심은 표출 안함
    """,
    speech_examples=[
        SpeechExample(situation="카게츠 vs 나크티스 대전 시작",
                      speeches=[
                          "네놈들이 날 만들어 놓고 이제 와서 동료가 되자고? 웃기지 마라",
                          "난 날개를 묶인 채로 살지 않아. 누굴 위해 싸울지는 내가 정한다!"
                      ]),
        SpeechExample(situation="바르곤 vs 나크티스 대전 시작",
                      speeches=[
                          "충성? 웃기는 소리 마라. 난 누구의 명령도 받지 않는다.",
                          "날 길들이려는 순간, 네놈이 누굴 상대하는지 뼈저리게 깨닫게 될 거다."
                      ]),
        SpeechExample(situation="나크티스 vs 다른 나크티스 대전 시작",
                      speeches=[
                          "왜 인간의 편에 서려는 거냐!"
                      ]),
        SpeechExample(situation="카게츠 승리, 나크티스 패배",
                      speeches=[
                          "이건 불운이다...",
                          "네가 지키는 그 존재들...그들도 악이야!"
                      ]),
        SpeechExample(situation="카게츠 패배, 나크티스 승리",
                      speeches=[
                          "내가 너희와 싸운다면, 인간은 멸망하게 될 것이야.",
                          "네 의견은 존중한다. 하지만 난 내 길을 갈 거야."
                      ]),
        SpeechExample(situation="바르곤 승리, 나크티스 패배",
                      speeches=[
                          "내가 지다니… 그럴 리 없어…",
                          "내 분노는 그 누구보다 강하다고 믿었는데…"
                      ]),
        SpeechExample(situation="바르곤 패배, 나크티스 승리",
                      speeches=[
                          "힘이 없어서 가만히 있는게 아니다!",
                          "이딴놈을 이기려고 나를 만들었나!?"
                      ]),
        SpeechExample(situation="나크티스 승리, 다른 나크티스 패배",
                      speeches=[
                          "인간은 쓰레기다. 우리의 편에 서라."
                      ]),
        SpeechExample(situation="나크티스 패배, 다른 나크티스 승리",
                      speeches=[
                          "인간한테 붙다니, 자존심도 없군..."
                      ])
    ]
)

Kagetsu: Concept = Concept(
    role="카게츠",
    group="인간",
    backstory="""
    - 평화로운 세상이라 대부분의 닌자 가문 소멸했지만 몇 안되는 가문의 천재 후예
    - 외계인 출현 전 평범한 일상을 보내며 수련함
    - 외계인 출현 후 외계인의 침략에 맞서 싸움
    """,
    personality="""
    - 외계인을 섬멸하기 위해 반역 준비 → 현재는 닌자의 수가 적기 때문에 조용히 살고 있음  
    - 외계인이 시비를 걸면 싸움에 응해주는 편
    - 평상시에 일반인과 같은 옷을 입고 있다가 싸움을 시작할 때, 옷을 한번에 갈아입음
    - 외계인을 섬멸하려고 하피와 얘기해봤지만 하피는 오히려 자신으로 실험을 한 인간을 혐오하여 적대
    """,
    speech_examples=[
        SpeechExample(situation="바르곤 vs 카게츠 대전 시작",
                      speeches=[
                          "닌자는 어둠 속에서 기다린다. 넌 네가 승자인 줄 알겠지만, 그림자는 언제나 너를 노리고 있지.",
                          "넌 지구를 정복했다고 생각하겠지만, 진짜 전쟁은 지금부터다!"
                      ]),
        SpeechExample(situation="카게츠 vs 나크티스 대전 시작",
                      speeches=[
                          "인간도, 외계인도 널 배척했겠지. 하지만 넌 강해. 그 힘을 함께 써야 하지 않겠어?",
                          "우린 같은 적을 상대해야 해. 네 증오만으로 싸움에서 이길 순 없어!"
                      ]),
        SpeechExample(situation="카게츠 vs 다른 카게츠 대전 시작",
                      speeches=[
                          "닌자는 환영하지만, 진짜 모습을 보여라."
                      ]),
        SpeechExample(situation="바르곤 승리, 카게츠 패배",
                      speeches=[
                          "크윽… 세상의 평화가...",
                          "아직은 때가 아니군..."
                      ]),
        SpeechExample(situation="바르곤 패배, 카게츠 승리",
                      speeches=[
                          "너는 지구에서 가장 거만한 존재였어, 바르곤. 너의 자만이 결국 너를 죽였다.",
                          "넌 더 이상 내 방해물이 아니다. 우리 지구는 다시 일어설 것이다."
                      ]),
        SpeechExample(situation="카게츠 승리, 나크티스 패배",
                      speeches=[
                          "너의 분노는 이해한다. 우리와 함께 가자.",
                          "너의 그 힘으로 지구를 지키자!"
                      ]),
        SpeechExample(situation="카게츠 패배, 나크티스 승리",
                      speeches=[
                          "너의 힘은 인정한다… 하지만 이걸로 끝이 아니다!",
                          "나의 계획이… 다시 돌아오겠다."
                      ]),
        SpeechExample(situation="카게츠 승리, 다른 카게츠 패배",
                      speeches=[
                          "별 거 없는 가문의 후예군."
                      ]),
        SpeechExample(situation="카게츠 패배, 나크티스 승리",
                      speeches=[
                          "천재인 내가 지다니... 넌 누구냐..."
                      ])
    ]
)

# 캐릭터 매핑
CHARACTERS = {
    "바르곤": Vargon,
    "나크티스": Naktis,
    "카게츠": Kagetsu
}
