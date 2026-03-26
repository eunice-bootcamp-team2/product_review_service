document.addEventListener("DOMContentLoaded", function () {
    const productList = document.getElementById("productList");
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const pageInfo = document.getElementById("pageInfo");

    let currentPage = 1;
    let nextPageExists = false;

    function getAccessToken() {
        return localStorage.getItem("access");
    }

    function getAuthHeaders() {
        const token = getAccessToken();

        if (!token) {
            return {};
        }

        return {
            Authorization: `Bearer ${token}`
        };
    }

    // =========================
    // [기존] 상품별 리뷰 조회
    // =========================
    async function fetchReviewsByProduct(productId) {
        try {
            const response = await axios.get(`/reviews/?product=${productId}`, {
                headers: getAuthHeaders()
            });

            const data = response.data;

            if (Array.isArray(data)) {
                return data;
            }

            if (Array.isArray(data.results)) {
                return data.results;
            }

            return [];
        } catch (error) {
            console.error(`상품 ${productId} 리뷰 불러오기 실패:`, error.response?.data || error);
            return [];
        }
    }

    // =========================
    // [추가] 리뷰별 댓글 목록 조회
    // GET /interactions/comments/<review_id>/
    // =========================
    async function fetchCommentsByReview(reviewId) {
        try {
            const response = await axios.get(`/interactions/comments/${reviewId}/`, {
                headers: getAuthHeaders()
            });

            const data = response.data;

            if (Array.isArray(data)) {
                return data;
            }

            if (Array.isArray(data.results)) {
                return data.results;
            }

            return [];
        } catch (error) {
            console.error(`리뷰 ${reviewId} 댓글 불러오기 실패:`, error.response?.data || error);
            return [];
        }
    }

    // =========================
    // [기존] 좋아요 토글
    // =========================
    async function toggleLike(reviewId) {
        return await axios.post(
            `/interactions/like/${reviewId}/`,
            {},
            {
                headers: getAuthHeaders()
            }
        );
    }

    // =========================
    // [기존] 북마크 토글
    // =========================
    async function toggleBookmark(reviewId) {
        return await axios.post(
            `/interactions/bookmark/${reviewId}/`,
            {},
            {
                headers: getAuthHeaders()
            }
        );
    }

    // =========================
    // [기존] 댓글 작성
    // POST /interactions/comment/<review_id>/
    // =========================
    async function createComment(reviewId, content) {
        return await axios.post(
            `/interactions/comment/${reviewId}/`,
            { content: content },
            {
                headers: {
                    "Content-Type": "application/json",
                    ...getAuthHeaders()
                }
            }
        );
    }

    // =========================
    // [기존] 신고 작성
    // POST /interactions/report/<review_id>/
    // =========================
    async function createReport(reviewId, reason) {
        return await axios.post(
            `/interactions/report/${reviewId}/`,
            { reason: reason },
            {
                headers: {
                    "Content-Type": "application/json",
                    ...getAuthHeaders()
                }
            }
        );
    }

    // =========================
    // [추가] 댓글 HTML 생성
    // =========================
    function createCommentHTML(comment) {
        return `
            <div class="comment-item" style="padding:6px 0; border-top:1px solid #eee;">
                <strong>${comment.username || "익명"}</strong>
                <span class="muted" style="margin-left:6px;">
                    ${comment.created_at ? new Date(comment.created_at).toLocaleString() : ""}
                </span>
                <div style="margin-top:4px;">${comment.content || ""}</div>
            </div>
        `;
    }

    // =========================
    // [수정] 리뷰 HTML 생성
    // 댓글 영역 표시 추가
    // =========================
    function createReviewHTML(review, productId, commentsHTML = "") {
        return `
            <div class="review-item" data-review-id="${review.id}" data-product-id="${productId}">
                <div class="review-top">
                    <strong>${review.username || review.user_name || "익명"}</strong>
                    <span class="muted">평점: ${review.rating ?? "-"}</span>
                </div>

                <p class="review-content">${review.content || ""}</p>

                <div class="review-actions">
                    <button type="button" class="like-btn action-btn">
                        <span class="action-label">
                            ${review.is_liked ? "💖 취소" : "🤍 좋아요"}
                        </span>
                        <span class="action-count">${review.likes_count ?? 0}</span>
                    </button>

                    <button type="button" class="bookmark-btn action-btn">
                        <span class="action-label">
                            ${review.is_bookmarked ? "🔖 취소" : "📑 북마크"}
                        </span>
                        <span class="action-count">${review.bookmarks_count ?? 0}</span>
                    </button>

                    <button type="button" class="report-btn action-btn report-action-btn">
                        <span class="action-label">🚨 신고하기</span>
                    </button>
                </div>

                <div class="comment-form" style="margin-top:10px; display:flex; gap:6px;">
                    <input
                        type="text"
                        class="comment-input"
                        placeholder="댓글을 입력하세요"
                        style="flex:1;"
                    >
                    <button type="button" class="comment-btn">댓글 등록</button>
                </div>

                <!-- [추가] 댓글 목록 렌더링 영역 -->
                <div class="comment-list" style="margin-top:10px;">
                    ${commentsHTML || `<p class="muted">등록된 댓글이 없습니다.</p>`}
                </div>
            </div>
        `;
    }

    // =========================
    // [추가] 리뷰 + 댓글까지 묶어서 HTML 생성
    // =========================
    async function buildReviewsHTML(productId) {
        const reviews = await fetchReviewsByProduct(productId);

        if (reviews.length === 0) {
            return `<p class="muted">등록된 리뷰가 없습니다.</p>`;
        }

        const reviewHtmlList = await Promise.all(
            reviews.map(async (review) => {
                const comments = await fetchCommentsByReview(review.id);
                const commentsHTML = comments.length > 0
                    ? comments.map(createCommentHTML).join("")
                    : `<p class="muted">등록된 댓글이 없습니다.</p>`;

                return createReviewHTML(review, productId, commentsHTML);
            })
        );

        return reviewHtmlList.join("");
    }

    // =========================
    // [수정] 특정 상품 카드 안 리뷰영역 새로고침
    // 리뷰 + 댓글 같이 다시 그림
    // =========================
    async function refreshReviewBox(card, productId) {
        const reviewBox = card.querySelector(".review-box");
        if (!reviewBox) {
            return;
        }

        const reviewsHTML = await buildReviewsHTML(productId);

        reviewBox.innerHTML = `
            <h4>리뷰</h4>
            ${reviewsHTML}
        `;
    }

    // =========================
    // [수정] 상품 카드 생성
    // 리뷰 + 댓글 같이 렌더링
    // =========================
    async function renderProductCard(product) {
        const card = document.createElement("div");
        card.className = "product-card";
        card.dataset.productId = product.id;

        const reviewsHTML = await buildReviewsHTML(product.id);

        card.innerHTML = `
            <a href="/products/${product.id}/" class="product-link">
                <img src="${product.image_url || ""}" alt="${product.name}" class="thumb">
                <h3>${product.name}</h3>
                <p class="muted">${product.description || ""}</p>
                <p><strong>${Number(product.price).toLocaleString()}원</strong></p>
            </a>

            <div class="review-box">
                <h4>리뷰</h4>
                ${reviewsHTML}
            </div>
        `;

        return card;
    }

    // =========================
    // [기존] 이벤트 위임
    // =========================
    productList.addEventListener("click", async function (event) {
        const likeBtn = event.target.closest(".like-btn");
        const bookmarkBtn = event.target.closest(".bookmark-btn");
        const commentBtn = event.target.closest(".comment-btn");
        const reportBtn = event.target.closest(".report-btn");

        if (likeBtn || bookmarkBtn || commentBtn || reportBtn) {
            event.preventDefault();
            event.stopPropagation();
        }

        if (likeBtn) {
            const reviewItem = likeBtn.closest(".review-item");
            const reviewId = reviewItem.dataset.reviewId;
            const productId = reviewItem.dataset.productId;
            const card = likeBtn.closest(".product-card");

            try {
                await toggleLike(reviewId);
                await refreshReviewBox(card, productId);
            } catch (error) {
                console.error("좋아요 에러:", error.response?.data || error);

                if (error.response?.status === 401) {
                    alert("로그인이 필요합니다.");
                    return;
                }

                alert("좋아요 처리에 실패했습니다.");
            }

            return;
        }

        if (bookmarkBtn) {
            const reviewItem = bookmarkBtn.closest(".review-item");
            const reviewId = reviewItem.dataset.reviewId;
            const productId = reviewItem.dataset.productId;
            const card = bookmarkBtn.closest(".product-card");

            try {
                await toggleBookmark(reviewId);
                await refreshReviewBox(card, productId);
            } catch (error) {
                console.error("북마크 에러:", error.response?.data || error);

                if (error.response?.status === 401) {
                    alert("로그인이 필요합니다.");
                    return;
                }

                alert("북마크 처리에 실패했습니다.");
            }

            return;
        }

        if (commentBtn) {
            const reviewItem = commentBtn.closest(".review-item");
            const reviewId = reviewItem.dataset.reviewId;
            const productId = reviewItem.dataset.productId;
            const card = commentBtn.closest(".product-card");
            const input = reviewItem.querySelector(".comment-input");

            const content = input.value.trim();

            if (!content) {
                alert("댓글 내용을 입력해주세요.");
                return;
            }

            try {
                await createComment(reviewId, content);

                input.value = "";
                alert("댓글이 등록되었습니다.");

                // [수정] 댓글도 등록 후 리뷰+댓글 전부 다시 렌더링
                await refreshReviewBox(card, productId);
            } catch (error) {
                console.error("댓글 등록 에러:", error.response?.data || error);

                if (error.response?.status === 401) {
                    alert("로그인이 필요합니다.");
                    return;
                }

                alert("댓글 등록에 실패했습니다.");
            }

            return;
        }

        if (reportBtn) {
            const reviewItem = reportBtn.closest(".review-item");
            const reviewId = reviewItem.dataset.reviewId;

            const reason = prompt("신고 사유를 입력해주세요.");

            if (!reason || !reason.trim()) {
                return;
            }

            try {
                await createReport(reviewId, reason.trim());
                alert("신고가 접수되었습니다.");
            } catch (error) {
                console.error("신고 에러:", error.response?.data || error);

                if (error.response?.status === 401) {
                    alert("로그인이 필요합니다.");
                    return;
                }

                alert("신고 처리에 실패했습니다.");
            }

            return;
        }
    });

    async function loadProducts(page = 1) {
        try {
            const response = await axios.get(`/products/api/?page=${page}`);
            const data = response.data;

            console.log("상품 응답:", data);

            productList.innerHTML = "";

            const products = Array.isArray(data) ? data : (data.results || []);

            if (products.length === 0) {
                productList.innerHTML = "<p>등록된 상품이 없습니다.</p>";
            } else {
                for (const product of products) {
                    const card = await renderProductCard(product);
                    productList.appendChild(card);
                }
            }

            currentPage = page;
            nextPageExists = !!data.next;

            pageInfo.textContent = `${currentPage} 페이지`;
            prevBtn.disabled = currentPage <= 1;
            nextBtn.disabled = !nextPageExists;

        } catch (error) {
            console.error("상품 목록 불러오기 에러:", error.response?.data || error);
            alert("상품 목록을 불러오지 못했습니다.");
        }
    }

    prevBtn.addEventListener("click", function () {
        if (currentPage > 1) {
            loadProducts(currentPage - 1);
        }
    });

    nextBtn.addEventListener("click", function () {
        if (nextPageExists) {
            loadProducts(currentPage + 1);
        }
    });

    loadProducts(1);
});
