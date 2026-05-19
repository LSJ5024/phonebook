$(function () {
  // 플래시 메시지 자동 닫기 (3초)
  setTimeout(function () {
    $('.alert.alert-success, .alert.alert-info').fadeOut('slow');
  }, 3000);

  // 컬러 input 미리보기 라벨 동기화
  $('input[type=color]').on('input', function () {
    $(this).next('span.color-preview').css('background', this.value);
  });

  // 테이블 행 클릭 → 상세 페이지 이동 (data-href 속성)
  $('tr[data-href]').css('cursor', 'pointer').on('click', function () {
    window.location = $(this).data('href');
  });

  // 검색창 엔터키 자동 제출
  $('#searchInput').on('keydown', function (e) {
    if (e.key === 'Enter') {
      $(this).closest('form').submit();
    }
  });

  // API 자동완성 (소속 필드)
  const orgInput = $('input[name=organization]');
  if (orgInput.length) {
    let debounceTimer;
    orgInput.on('input', function () {
      clearTimeout(debounceTimer);
      const val = this.value.trim();
      if (val.length < 2) return;
      debounceTimer = setTimeout(function () {
        fetch('/api/v1/contacts?q=' + encodeURIComponent(val))
          .then(r => r.json())
          .then(data => {
            const orgs = [...new Set(data.map(c => c.organization).filter(Boolean))];
            // 간단 datalist 업데이트
            let dl = document.getElementById('org-datalist');
            if (!dl) {
              dl = document.createElement('datalist');
              dl.id = 'org-datalist';
              orgInput[0].setAttribute('list', 'org-datalist');
              document.body.appendChild(dl);
            }
            dl.innerHTML = orgs.map(o => `<option value="${o}">`).join('');
          });
      }, 300);
    });
  }
});
