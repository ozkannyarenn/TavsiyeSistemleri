# TavsiyeSistemleri
Kullanıcının seçeneklere vereceği yanıtları tahmin etmeyi içeren kapsamlı web uygulamları sınıfına “Öneri Sistemleri” denilmektedir. 
Öneri Sistemleri, genellikle “Tavsiye Sistemleri” olarak da adlandırılmaktadır. 
Büyük miktarda veri bulunan havuzdan faydalı içerikleri filtreleyerek kullanıcıya yönelik en anlamlı ve doğru ürünleri sağlamayı amaçlayan algoritmalardır. 
Öneri Motorları (Recommendation Engines) da tüketicilerin seçimlerini öğrenerek veri setindeki veri desenlerini keşfeder ve kullanıcının ihtiyaçları ve ilgi alanları doğrultusunda sonuçlar üretir.

# Kullanıcı-Kullanıcı İşbirliğine Dayalı Filtreleme (User-User Collaborative Filtering)
Benzer müşteriler ilişkilendirilmeye çalışılır ve müşterilerin seçtiği ürünlere dayanarak ürünler sunulur. Oldukça etkilidir fakat zaman ve kaynak gerektirir. 
Bu filtreleme türü, her iki müşteri tipinin bilgisini analiz etmeyi gerektirir. Bu nedenle, büyük platformlar için bu algoritmayı uygulamak zordur.

# Öğe-Öğe İşbirliğine Dayalı Filtreleme (Item-Item Collaborative Filtering)
Önceki algoritmaya çok benzerdir fakat müşteriler arasında benzerlik bulmak yerine ürün benzerliğine odaklanır. 
Bu algoritma ile birlikte herhangi bir öğeyi satın alan müşteriye, benzer öğeleri kolaylıkla önerebiliriz. 
Kullanıcı-kullanıcı işbirliğine dayalı filtrelemeye kıyasla daha az kaynak ve zaman gerektirmektedir. Bu filtreleme çeşidine D&R’ın sistemini örnek verebiliriz.

# Hibrit Öneri Sistemleri (Hybrid Recommendation Systems)
Son araştırmalar, işbirlikçi ve içeriğe dayalı önerilerin birleştirilmesinin daha etkili olabileceğini göstermektedir. 
Hibrit yaklaşımlar, iki öneri sistemi ayrı ayrı yapılarak ve ardından birleştirilerek uygulanabilir. 
Ayrıca, işbirliğine dayalı bir yaklaşıma içerik tabanlı özellikler ekleyerek veya içerik tabanlı bir öneri sistemine işbirliğine dayalı özellikler ekleyerek bu yaklaşımlar tek modelde birleştirilebilmektedir. 
Hibrit öneri sisteminin performansı saf işbirlikçi ve içerik temelli yöntemlerle karşılaştırmaya odaklanan birkaç çalışma yapılmış ve hibrit yöntemlerin saf yaklaşımlardan daha doğru tavsiyeler sunabileceği kanıtlanmıştır. 
Hibrit öneri sistemi, veri yetersizliği gibi yaygın sorunların üstesinden gelmek için kullanılabilir.
