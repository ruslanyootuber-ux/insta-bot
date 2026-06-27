// Server manzili (Fly.io dagi ilovangiz manzili)
const API_BASE_URL = "https://insta-bot.fly.dev/";

// Tugmalar bosilganda ishga tushadigan umumiy funksiya
async function handleMenuClick(action) {
    try {
        // Serverdan ma'lumot so'rash
        const response = await fetch(`${API_BASE_URL}/api/${action}`);
        const data = await response.json();
        
        // Bu yerda kelgan ma'lumotni ekranga chiqarish logikasi bo'ladi
        console.log(`${action} bo'yicha ma'lumot:`, data);
        
        // Misol: Agar ma'lumot hadis bo'lsa, alert oynasida ko'rsatish
        if(data.matn) {
            alert(data.matn);
        }
    } catch (error) {
        console.error("Xatolik:", error);
        alert("Ma'lumotni yuklashda xatolik yuz berdi.");
    }
}

// Barcha tugmalarni bog'lash
document.querySelectorAll('.menu-item').forEach((item, index) => {
    item.addEventListener('click', () => {
        const actions = ['namoz', 'asmaul', 'tasbeh', 'qibla', 'zikr', 'ramazon', 'hadis', 'eslatma', 'mazhab', 'boglanish', 'baholash', 'ulashish'];
        handleMenuClick(actions[index]);
    });
});