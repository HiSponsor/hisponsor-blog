"""
HiSponsor - AI 자동 포스팅 스크립트
Claude API를 사용하여 정보글을 자동 생성하고
information.html에 추가합니다.
"""

import anthropic
import os
import re
from datetime import datetime

# =============================================
# 🔧 설정 값 (필요시 수정하세요)
# =============================================

# 포스팅 주제 목록 (매주 순환)
TOPICS = [
    "2025년 취업 비자 최신 트렌드와 주의사항",
    "스폰서 기업이 원하는 인재상과 준비 방법",
    "한국에서 외국인이 취업하는 현실적인 방법",
    "E-7 비자 신청 시 자주 하는 실수 TOP 5",
    "스폰서십 인터뷰에서 합격하는 전략",
    "취업 비자와 워킹홀리데이 비자 비교 분석",
    "한국 스타트업에서 일하는 외국인 인터뷰",
    "링크드인으로 스폰서 기업 찾는 실전 가이드",
]

# 날짜로 주제 자동 선택 (매주 다른 주제)
week_number = datetime.now().isocalendar()[1]
auto_topic = TOPICS[week_number % len(TOPICS)]

# 환경변수에서 주제 가져오기 (수동 실행 시 입력값 사용)
topic = os.environ.get('POST_TOPIC', '').strip() or auto_topic

print(f"📝 이번 주 주제: {topic}")

# =============================================
# Claude API로 글 생성
# =============================================

client = anthropic.Anthropic(api_key=os.environ['ANTHROPIC_API_KEY'])

prompt = f"""
당신은 HiSponsor 사이트의 콘텐츠 작성자입니다.
아래 주제로 취업/스폰서십 관련 유용한 정보 글을 작성해주세요.

주제: {topic}

작성 규칙:
1. 실용적이고 구체적인 정보 위주
2. 300~500자 내외
3. 아래 HTML 형식으로만 출력 (다른 설명 없이)
4. 한국어로 작성

출력 형식 (이 형식 그대로):
<제목>여기에 제목 작성</제목>
<태그>비자 정보|취업 팁|스폰서십|뉴스 중 하나</태그>
<내용>
<p>첫 번째 단락...</p>
<p>두 번째 단락...</p>
<ul>
  <li>항목 1</li>
  <li>항목 2</li>
</ul>
<p>마무리 문장...</p>
</내용>
"""

print("🤖 Claude API 호출 중...")

message = client.messages.create(
    model="claude-opus-4-5",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

response_text = message.content[0].text
print("✅ 글 생성 완료!")

# =============================================
# 응답 파싱
# =============================================

title_match = re.search(r'<제목>(.*?)</제목>', response_text, re.DOTALL)
tag_match = re.search(r'<태그>(.*?)</태그>', response_text, re.DOTALL)
content_match = re.search(r'<내용>(.*?)</내용>', response_text, re.DOTALL)

title = title_match.group(1).strip() if title_match else topic
tag = tag_match.group(1).strip() if tag_match else "정보"
content = content_match.group(1).strip() if content_match else f"<p>{response_text}</p>"

# 날짜 포맷
now = datetime.now()
day = now.strftime('%d')
month_en = now.strftime('%b').upper()
year = now.strftime('%Y')
date_str = f"{year}.{now.strftime('%m')}.{day}"

# 태그 색상 결정
tag_class = {
    "비자 정보": "tag-blue",
    "취업 팁": "tag-green",
    "스폰서십": "tag-green",
    "뉴스": "tag-gray"
}.get(tag, "tag-gray")

# =============================================
# information.html에 새 포스트 삽입
# =============================================

new_post_html = f"""
        <!-- AI 자동 생성 포스트 - {date_str} -->
        <div class="post-full">
          <div class="post-header">
            <div class="post-date">
              <span class="day">{day}</span>
              <span class="month">{month_en} {year}</span>
            </div>
            <div style="flex:1;">
              <div style="margin-bottom:8px;">
                <span class="tag {tag_class}">{tag}</span>
                <span class="tag tag-gray" style="margin-left:4px;">🤖 AI 작성</span>
              </div>
              <h3 style="font-size:1.1rem; font-weight:700; margin-bottom:6px;">{title}</h3>
              <button class="toggle-btn" onclick="togglePost(this)">자세히 보기 ▼</button>
            </div>
          </div>
          <div class="post-body">
            {content}
          </div>
        </div>
"""

# information.html 읽기
with open('information.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 지정 위치에 새 포스트 삽입
# <!-- AI 자동 포스팅 글이 여기에 추가됩니다 --> 위에 삽입
marker = '        <!-- AI 자동 포스팅 글이 여기에 추가됩니다 -->'
if marker in html_content:
    html_content = html_content.replace(marker, new_post_html + '\n' + marker)
else:
    # 마커가 없으면 </section> 직전에 삽입
    html_content = html_content.replace('      </div>\n    </section>\n\n  </main>', 
                                         new_post_html + '      </div>\n    </section>\n\n  </main>')

# 파일 저장
with open('information.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

# posts/ 폴더에도 별도 백업
os.makedirs('posts', exist_ok=True)
backup_filename = f"posts/{now.strftime('%Y-%m-%d')}-auto-post.html"
with open(backup_filename, 'w', encoding='utf-8') as f:
    f.write(f"<!-- {date_str} AI 자동 생성 -->\n{new_post_html}")

print(f"✅ information.html 업데이트 완료!")
print(f"📁 백업 파일: {backup_filename}")
