// Server manzili (Fly.io dagi ilovangiz manzili)
// Eslatma: Fly.io da ilovangiz nomi qanday bo'lsa, o'shani yozing
const API_BASE_URL = "https://insta-bot.fly.dev";

async function handleMenuClick(action) {
    try {
        // API dan ma'lumotni so'rash
        const response = await fetch(`${API_BASE_URL}/api/${action}`);
        
        if (!response.ok) {
            throw new Error('Serverdan ma\'lumot kelmadi');
        }
        
        const data = await response.json();
        
        // Bu yerda kelgan ma'lumotni ekranga chiqarish mantig'i
        console.log(`${action} bo'yicha ma'lumot:`, data);
        
        // Misol uchun alert orqali ko'rsatamiz (keyinchalik buni chiroyli oynaga almashtiramiz)
        alert(JSON.stringify(data, null, 2));
        
    } catch (error) {
        console.error("Xatolik:", error);
        alert("Kechirasiz, hozircha bu bo'lim ishlamayapti yoki serverda xatolik bor.");
    }
}

// Barcha menyu tugmalariga bosilganda ishlaydigan hodisani bog'lash
// index.html dagi .menu-item klassiga ega elementlarni qidirib topamiz
document.querySelectorAll('.menu-item').forEach((item, index) => {
    item.addEventListener('click', () => {
        // HTML'dagi ketma-ketlik bo'yicha action nomlari
        const actions = [
            'namoz', 'asmaul', 'tasbeh', 'qibla', 'zikr', 
            'ramazon', 'hadis', 'eslatma', 'mazhab', 
            'boglanish', 'baholash', 'ulashish'
        ];
        
        const action = actions[index];
        if (action) {
            handleMenuClick(action);
        }
    });
});
