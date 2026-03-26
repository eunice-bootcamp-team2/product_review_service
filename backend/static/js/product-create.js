document.addEventListener("DOMContentLoaded", () => {

    const form = document.getElementById("productCreateForm");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const name = document.getElementById("name").value;
        const description = document.getElementById("description").value;
        const price = document.getElementById("price").value;
        const image = document.getElementById("image").files[0];

        const formData = new FormData();

        formData.append("name", name);
        formData.append("description", description);
        formData.append("price", price);

        if (image) {
            formData.append("image", image);
        }

        try {

            const response = await axios.post("/products/api/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data"
                }
            });

            alert("상품이 등록되었습니다.");
            window.location.href = "/products/";

        } catch (error) {
            console.error(error);
            alert("상품 등록 실패");
        }

    });

});
