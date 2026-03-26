document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("productUpdateForm");
    const updateBtn = document.getElementById("btn-primary");

    const nameInput = document.getElementById("name");
    const descriptionInput = document.getElementById("description");
    const priceInput = document.getElementById("price");
    const imageInput = document.getElementById("image");
    const imagePreview = document.getElementById("imagePreview");

    // 현재 URL 예: /products/15/update/
    const pathParts = window.location.pathname.split("/").filter(Boolean);
    const productId = pathParts[1]; // ["products", "15", "update"]

    console.log("현재 productId:", productId);

    async function loadProduct() {
        try {
            const response = await axios.get(`/products/api/${productId}/`);
            const product = response.data;

            console.log("불러온 상품 데이터:", product);

            nameInput.value = product.name || "";
            descriptionInput.value = product.description || "";
            priceInput.value = product.price || "";

            if (product.image || product.image_url) {
                imagePreview.src = product.image_url || product.image;
                imagePreview.style.display = "block";
            } else {
                imagePreview.style.display = "none";
            }
        } catch (error) {
            console.error("상품 정보 조회 실패:", error.response?.data || error);
            alert("상품 정보를 불러오지 못했습니다.");
        }
    }

    if (imageInput) {
        imageInput.addEventListener("change", function () {
            const file = imageInput.files[0];

            if (!file) {
                return;
            }

            const reader = new FileReader();
            reader.onload = function (event) {
                imagePreview.src = event.target.result;
                imagePreview.style.display = "block";
            };
            reader.readAsDataURL(file);
        });
    }

    // 버튼 클릭 확인용
    if (updateBtn) {
        updateBtn.addEventListener("click", function () {
            console.log("수정 완료 버튼 클릭");
        });
    }

    // 실제 저장 처리
    if (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            console.log("폼 submit 실행");

            try {
                const formData = new FormData();
                formData.append("name", nameInput.value.trim());
                formData.append("description", descriptionInput.value.trim());
                formData.append("price", priceInput.value.trim());

                if (imageInput.files.length > 0) {
                    formData.append("image", imageInput.files[0]);
                }

                const response = await axios.patch(
                    `/products/api/${productId}/`,
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data"
                        }
                    }
                );

                console.log("상품 수정 성공:", response.data);
                alert("상품이 수정되었습니다.");

                window.location.href = `/products/${productId}/`;
            } catch (error) {
                console.error("상품 수정 실패:", error.response?.data || error);
                alert("상품 수정에 실패했습니다.");
            }
        });
    }

    loadProduct();
});
