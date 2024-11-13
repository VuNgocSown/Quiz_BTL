from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from quiz.models import Quiz, Document  # Import models from 'search'
import unidecode  # Thư viện để chuyển đổi tiếng Việt có dấu thành không dấu
from fuzzywuzzy import process  # Thư viện để tìm gợi ý từ khóa
from allClass.models import MyClass
from .models import SearchHistory
@login_required(login_url='login')
def search(request,class_id):
    query = request.GET.get('q', '').strip()
    content_type = request.GET.get('content_type', 'all')  # Lấy loại nội dung (tài liệu, video)
    page_number = request.GET.get('page', 1)
    no_results_message = None
    suggestion = None
    results = None

    # Nếu không có từ khóa tìm kiếm, trả về trang kết quả rỗng
    if not query:
        return render(request, 'search/search_results.html', {
            'results': {}, 
            'query': query,
            'content_type': content_type
        })

    # Chuyển từ khóa thành dạng không dấu để tìm kiếm tiếng Việt không dấu
    query_no_diacritics = unidecode.unidecode(query)

    # Tìm kiếm trên nhiều trường của các model
    document = Document.objects.filter(
        Q(title__icontains=query) | Q(description__icontains=query) |
        Q(title__icontains=query_no_diacritics) | Q(description__icontains=query_no_diacritics),
        myclass=class_id
    )
    quiz = Quiz.objects.filter(
        Q(title__icontains=query) |  Q(description__icontains=query) |
        Q(title__icontains=query_no_diacritics) | Q(description__icontains=query_no_diacritics),
        class_id=class_id
    )

    # Nếu không tìm thấy bất kỳ kết quả nào, tìm gợi ý từ khóa gần đúng nhất
    if not document.exists() and not quiz.exists():
        all_titles = [d.title for d in Document.objects.filter(myclass=class_id)] + [q.title for q in Quiz.objects.filter(class_id=class_id)]
        closest_match = process.extractOne(query, all_titles)
        if closest_match and closest_match[1] >= 60:  # Ngưỡng độ chính xác cho gợi ý
            suggestion = closest_match[0]
            no_results_message = f"Không có dữ liệu nào phù hợp với từ khóa '{query}'. Gợi ý: bạn có muốn tìm '{suggestion}' không?"
        else:
            no_results_message = f"Không có dữ liệu nào phù hợp với từ khóa '{query}'."
        return render(request, 'search/search_results.html', {
            'results': None,
            'query': query,
            'content_type': content_type,
            'no_results_message': no_results_message,
            'suggestion': suggestion,
            'class_id': class_id
        })

    # Lưu lịch sử tìm kiếm nếu tìm thấy kết quả
    if document.exists() or quiz.exists():
        SearchHistory.objects.create(user=request.user, query=query)

    # Tổng hợp và phân trang kết quả
    if content_type == 'document':
        results = list(document)
    elif content_type == 'quiz':
        results = list(quiz)
    else:
        # Giữ nguyên code cũ cho trường hợp 'all'
        results = list(document) + list(quiz)

    paginator = Paginator(results, 15)  # Tổng hợp các loại nội dung với 15 kết quả mỗi trang
    page_obj = paginator.get_page(page_number)

    return render(request, 'search/search_results.html', {
        'results': page_obj,
        'query': query,
        'content_type': content_type,
        'no_results_message': no_results_message,
        'suggestion': suggestion,
        'class_id': class_id
    })

@login_required(login_url='login')
def search_history(request, class_id):
    # Lấy lịch sử tìm kiếm của người dùng hiện tại và sắp xếp theo thời gian mới nhất
    history = SearchHistory.objects.filter(user=request.user, class_id=class_id).order_by('-timestamp')

    return render(request, 'search/search_history.html', {
        'history': history,
        'class_id': class_id
    })
