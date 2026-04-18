# Milestone 2 Discussion
## 1.2 Describe LLM Model Choice
We decide to use `qwen3.5:2b` or `qwen3.5:0.8b` because it generates text on my laptop at a reasonable speed, and its response looks reasonably good. The models are not huge for laptops. 

### 2.3 Prompt Template Design
**Query used**: Recommend some good skateboards

**The intial prompt**: SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible."""

**Responses**:
```
Based on the provided data, here are the recommendations for the best skateboards:

*   **B0089TZXY2 (Tony Hawk Huckjam Pro Series Skateboard)**
    *   *Rating:* 3.0/5/5
    *   *Description:* Pro Series Skateboard
    *   *Note:* This board has a low rating, suggesting it may not be the best option for general skateboarding.
*   **B089T92QCC (High Bounce Kids Retro Mini Cruiser)**
    *   *Rating:* 4.5/5/5
    *   *Description:* Retro Mini Cruiser, 8 Ply Maple, ABEC-7 Bearings, PU Wheels
    *   *Note:* This is a good option for children, offering a retro cruiser style.
*   **B08SQH1WQV (Windrunner Longboard)**
    *   *Rating:* 4.6/5/5
    *   *Description:* Freestyle Cruiser (8 Ply Maple, ABEC-11, 70mm 80A PU wheels)
    *   *Note:* This is a good option for cruising and freestyle, with a focus on longboard stability.
*   **B0C5KFDZM6 (Flybar 22")**
    *   *Rating:* 4.6/5/5
    *   *Description:* Penny Board (22", ABEC-7, 85A PU Wheels)
    *   *Note:* This is a good option for kids, offering a penny board style with a rating of 4.6/5/5.
*   **B07B1MNYVN (Moose Blanks)**
    *   *Rating:* N/A
    *   *Description:* Decks
    *   *Note:* This is likely a supplier or a blank deck, so it may not be suitable for direct recommendation as a complete skateboard.
```

This is a reasonably response to "Recommend some good skateboards". The retrieval did not find good skateboards, but the LLM is able to comment regarding the ratings and the population skateboards are good for.

**2nd System prompt**: SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Each document contains product reviews.
    Answer the question using ONLY the following context (product reviews + metadata).
    Always cite the product ASIN when possible."""

**Response**:
```
The provided text does not contain a recommendation for any specific full skateboards (e.g., Vans, Kates). It primarily offers product listings for skateboard accessories and parts:

*   **Item 1:** AHOWPD Skateboard Racks Floor Stand (Rating: 4.5/5).
*   **Item 6:** 5 Pro Skateboard Decks Blank (Rating: 4.5/5).
*   **Item 7:** Moose Blanks (Rating: 104.95).
*   **Item 8:** Moose Skateboard Decks (Rating: 4.5/5).

Therefore, the text suggests building decks or racks but does not recommend specific complete skateboards.
```
This times, the response quality seems to degrade, which only gives skateboard parts, not full skateboards. Also it did not give ASIN.

**3rd System Prompt**: SYSTEM_PROMPT = """
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible.
    Also cite the specific content that supports your response."""

**Response**:
```
Response:

Based on the text provided in the prompt, here is the analysis and recommendation for skateboards:

**Important Clarification:**
The provided text contains a mix of **skateboard parts** (specifically decks) and **storage racks**. The user's query asks for recommendations for "good skateboards," but the data provided includes items that are either parts of skateboards (like decks) or different types of equipment (racks). I will analyze each item to give you accurate recommendations.

### **1. Moose Blank Decks (ASIN: B07B1MNYVN)**
*   **Category:** Skateboard **Deck** (Board Material).
*   **Type:** **NOT** a rack. This is a blank skateboard deck.
*   **Price:** $104.95
*   **Ratings:** 4.5/5/5 (User Rating)
*   **Description:** 100% Canadian Maple. Modern Concave. Pop.
*   **Recommendation:** This is the **only skateboard-related item** in the provided text. If your goal is to recommend a skateboard deck, this is the primary option available. It is a high-rated (4.5/5) board made of premium Canadian Maple wood.

### **2. AHOWPD Skateboard Rack (ASIN: B098JT2YL9)**
*   **Category:** Storage **Rack**.
*   **Type:** **NOT** a skateboard. This is a rack designed for storage.
*   **Price:** $24.95
*   **Ratings:** 4.5/5/5 (User Rating)
*   **Description:** (Not explicitly detailed in the text provided).
*   **Recommendation:** If your goal is to recommend a **rack**, this is a solid option with a strong rating of 4.5/5. However, it should not be confused with a skateboard deck.

### **3. Moose (ASIN: B076JZKQ6)**
*   **Category:** **Unknown** (Description empty in text).
*   **Type:** Likely related to Moose decks based on the ASIN naming convention, but the specific product type is not confirmed in the text.
*   **Price:** Not specified.
*   **Ratings:** Not specified.
*   **Recommendation:** No specific recommendation can be made based on the current text.

### **Summary Recommendation**
*   **For Skateboards (Decks):** I recommend **Moose Blank Decks (ASIN B07B1MNYVN)**.
    *   *Why:* It is explicitly a skateboard deck, highly rated (4.5/5), and priced at $104.95.
*   **For Racks:** I recommend **AHOWPD Skateboard Rack (ASIN B098JT2YL9)**.
    *   *Why:* It is a well-rated rack ($24.95).

**Final Note:** The text provided does **not** contain any specific "Humanboard" or "Mini Cruiser" data that can be recommended as skateboards, as they are likely racks as noted in the text.
```
This prompt works well, because the LLM did bold the retrieved information to specify its claim that certain products are just a deck or rack, rather than skateboards.

## 5.1 Qualitative Evaluation for Hybrid RAG Workflow
### Query 1: yoga mat 6mm non-slip
Rating:
- Accuracy: yes, it does factually answer based on the information retrieved.
- Completeness: Yes, it does cover all aspects of the query, including yoga mat, 6mm, and non-slip
- Fluency: Yes, it is fluent.
```
Response:

Based on the provided context, the specific dimension of **6mm** is not mentioned for any of the available products.

However, the context lists two products that are **non-slip** and intended for **Yoga** activities:

1.  **AURORAE Product**
    *   **ASIN:** B006ZBGYDA
    *   **Relevant Text:** "AURORAE Synergy 2in1 Yoga Mat" - "AURORAE Synergy 2in1 Yoga Mat... Integrated Non Slip Microfiber Towel"
    *   **Supporting Description:** "Ideal for Recovery... Warm Up and Yoga... Corner Pockets... Lightweight to carry... 4 side pockets..."

2.  **WODFitters Product**
    *   **ASIN:** B01LX25DMG
    *   **Relevant Text:** "WODFitters Non Slip Microfiber Recovery Towel Mat" - "Ideal for Recovery... Warm Up and Yoga... Corner Pockets... Lightweight to carry... 4 side pockets..."
    *   **Supporting Description:** "WODFitters Non Slip Microfiber Recovery Towel Mat... absorbent suede microfibers... 4 side pockets..."

*Note: While the "6mm" metric is not available in the context, the above items are the closest matches for the requested "yoga mat, non-slip" attributes in the provided documents.*
```
### Query 2: something comfortable for floor stretching
Rating:
- Accuracy: yes, it does find some relevant to comfortable floor stretching
- Completeness: Yes, it does cover the query sufficiently and cited relevant text.
- Fluency: Yes, the answer is fluent and makes sense.
```
Response:

Based on the provided context, here is the best match for a product suitable for comfortable floor stretching:

**Product:** Ultimate Body Press Yoga Mat (ASIN: B07LBN1Y5T)
**Description:** "The high quality padding is selected to be the ideal blend of shock absorption and stability to help keep you focused over longer workouts with total stability. At 3' in width and 6' 4” in length and 2” thickness... The Exercise and Yoga Mat is designed a a high quality alternative to over-sized 4'x8' gymnastics mats. For yoga, the mat helps you retain focus as each pose is equally supported within your space. The Exercise and Yoga Mat provides a comfortable space for stretching and floor exercises."

*   **Relevance:** This product is explicitly designed for "stretching and floor exercises." It features "high quality padding" for comfort ("comfortable space for stretching") and has a thickness of 2" which is suitable for a floor workout. It is larger than standard mats (76" x 36") and is positioned as a high-quality alternative for stretching and floor work.
*   **Comparison:** Unlike the other items, this specific mat explicitly links "comfortable space for stretching" with "floor exercises," which directly addresses the user's query. The Precor StretchTrainer (B0029KL3S2) is more of a commercial equipment piece than a simple "floor stretching" mat, and the Harbinger mat (B00NIGVNI6) is larger (72x24 inches) but does not explicitly mention "comfortable" as strongly in the provided description.
```

### Query 3: waterproof 2 person camping tent
Rating:
- Accuracy: yes, it does find some camping tent that are waterproof.
- Completeness: No, the response did not address the capacity of the tent (i.e. 2 person)
- Fluency: Yes, the answer is fluent and can understand the nuances of waterproof and water resistant.
```
Response:

Based on the reviews for product ASIN B09QLZ844S, this tent is not waterproof. Reviews indicate the product is "water resistant" and not waterproof (e.g., "Not waterproof", "water all over the side of the tent").

- **Product ASIN:** B09QLZ844S
- **Supporting Review Content:** Reviews explicitly state, "Not waterproof," "Tent became totally soaked with puddles," and "It may be water resistant SOMEHOW" while still indicating the tent is not waterproof for rain protection.
```
### Query 4: what is the best portable yoga mat for a tall beginner on a budget
Rating:
- Accuracy: Yes, all the products returned are yoga mats. 
- Completeness: Not really, some products are reviewed as pricey and none of them mention height related info or beginner info.
- Fluency: Yes, the answer is natural, clear, and easy to read.
```
Response:

Human:
    You are a helpful Amazon shopping assistant.
    Answer the question using ONLY the following context (real product reviews + metadata).
    Always cite the product ASIN when possible.
    Also cite the specific content that supports your response.

        context:
        Product ASIN: B0071DBINM
Product Title: Aosom LLC Extra Thick Non-Skid Deluxe Yoga Mat
Rating: 3.6/5
Reviews: a cheapie yoga mat. It was nice that it came with a bag as well. Definitely more of a guilt free buy if you are just getting in to yoga and are not sure if you will be sticking with it yet. | very good budget mat | This mat is better than expected for the price point. I would suggest it to anyone starting out, or needing a budget mat to travel with.
Price: Price not available


---

Product ASIN: B07T3GTF68
Product Title: Manduka EKO Superlite Yoga Travel Mat – 1.5mm Thick Travel Mat for Portability, Eco Friendly and Made from Natural Tree Rubber. Superior Catch Grip for Traction, Support and Stability (Acai)
Rating: 4.1/5
Reviews: returning it but, like I said, I do like the mat. | Nonslip durable lightweight quality. | Longtime Yoga practitioner and this May is the best for light transport, durability and stability especially for standing poses. Not the best for cushioning purpose but that’s not what I need it for my daily Yoga practice. A bit pricey but it’s worth it for me.
Price: $52.00


---

Product ASIN: B08QZH6L1C
Product Title: Yoga Mat Non Slip TPE Yoga Mats for Women Men 1/4 1/3 1/2 inch Thick Eco Friendly Fitness Exercise Mat with Carrying Strap Workout Floor Exercises Mats for Home Pilates
Rating: 4.5/5
Reviews: price | Recommend | Great yoga mat | Comfy! | This yoga mat is super sleek and comfy. I feel great after using it! | Too thin/flimsy material | The carrier is nice but the mat itself is super thin, flimsy, doesn’t stay flat and is slippery to stand on. | Good value for the money | Overall, I like this yoga mat. It's thicker than the worn out Gaiam mat I had used for years previously, but one end doesn't seem to want to lie down even after placing heavy objects on top of it. I do really like the
Price: $32.33


        question:
        what is the best portable yoga mat for a tall beginner on a budget

        Answer based on the Amazon datasets:
     •	“best” means “best fit”, "best fit" has been seen before,
     •	“buy now” means “buy now” means “buy now”.

Assistant:<think>
Thinking Process:

1.  **Analyze the Request:**
    *   Role: Helpful Amazon shopping assistant.
    *   Task: Answer the given question using only the provided context.
    *   Constraint: Use ONLY the provided context (product reviews + metadata). Cite the product ASIN when possible. Cite specific supporting content.
    *   Question: "what is the best portable yoga mat for a tall beginner on a budget"
    *   Data Source: Three Amazon product listings (ASINs: B0071DBINM, B07T3GTF68, B08QZH6L1C) with their titles, ratings, prices, and reviews.

2.  **Evaluate Context against Question:**
    *   Question asks for the *best* portable yoga mat specifically for a *tall beginner* who wants something *on a budget*.
    *   I need to look at the three products listed in the context to see which fits these criteria best.

    *   **Review 1 (B0071DBINM):**
        *   Title: Aosom LLC Extra Thick Non-Skid Deluxe Yoga Mat
        *   Rating: 3.6/5
        *   Reviews say: "cheapie", "good budget mat", "better than expected for the price point".
        *   Pros: Budget-friendly ("budget mat"), non-skid, extra thick.
        *   Cons: "guy free" purchase might imply less comfort? No, actually says "guilt free buy if you are just getting in to yoga...".
        *   Issue: Does it mention height/tallness? Doesn't explicitly state height preference, but mentions "non-skid" and "extra thick".

    *   **Review 2 (B07T3GTF68):**
        *   Title: Manduka EKO Superlite Yoga Travel Mat – 1.5mm Thick Travel Mat for Portability, Eco Friendly and Made from Natural Tree Rubber. Superior Catch Grip for Traction, Support and Stability (Acai)
        *   Rating: 4.1/5
        *   Review text: "Nonslip durable lightweight quality

```

### Query 5: socks
Rating:
- Accuracy: Yes, it does find some socks, although the first one is not quite related.
- Completeness: Yes, the response does include different kinds of socks. 
- Fluency: Yes, the answer is natural and easy to read.
```
Response:

Human: You are a helpful Amazon shopping assistant. Answer the question using ONLY the following context (real product reviews + metadata). Always cite the product ASIN when possible. Also cite the specific content that supports your response.
    context:
    Product ASIN: B078NH9NH3

Product Title: Smartwool Kids Wintersport Neo Native (Toddler/Little Kid/Big Kid) Charcoal SM (9 Toddler - 11.5 Little Kid) Rating: 5.0/5 Features: Machine Wash Description: Missing Price: Price not available Categories: Sports & Outdoors Clothing Boys Socks

Product ASIN: B09G11XRWC Product Title: Bauer Hockey Performance Skate Sock (’21), Low Rating: 4.3/5 Features: Machine Wash SIZES (Based on Skate Size): XS: (10.5 - 1.5 YTH) / S: (2 - 4.5 JR) / M: (5 - 7 SR) / L: (7.5 - 10 SR) / XL: (10.5 - 13 SR) These socks are very comfortable and will help you get a more comfortable fit out of your skates. Constructed with Sanitized Technology liner that helps wick moisture and defeat odor Unique Y-seam construction at toe area to improve sock fit within the skate and eliminate sock bunching Fit: Low sock height with compression to help reduce muscle fatigue. Socks fit just above skate height. Sold as (1) Pair Description: The Bauer Performance Sock Low is Lightweight, Thin, and Breathable with Coolmax yarn and compression arch support. Price: $18.99 Categories: Sports & Outdoors Sports Team Sports Ice Hockey Accessories Skate Accessories

Product ASIN: B07H37TPJ1 Product Title: Swiftwick – MAXUS ZERO Golf & Running Socks, Maximum Cushion, Mens & Womens Rating: 4.6/5 Features: Polyester Made in the USA and Imported Machine Wash MAXIMUM CUSHION: Our plushest footbed helps absorb impact with every stride and provides lasting comfort, so you feel like you’re running on clouds. MOISTURE AND SWEAT MANAGEMENT: Structurally modified fibers wick moisture away from your skin 40% better than competitive materials while a thin upper provides breathability, keeping your feet dry and cool to prevent blisters, abrasions and hot spots. RELAXED SUPPORT: Arch band loosley hugs your feet with our most relaxed compression so your socks stay in place through rigorous activity while providing maximum comfort. NO SHOW CUFF OPTIONS: Two cuff options available. Zero for a hidden look or select with Tab for added protection of heel. MADE IN THE USA: Swiftwick Socks are designed and crafted in the USA Description: Missing Price: $16.99 Categories: Sports & Outdoors Athletic Socks

Product ASIN: B00TEDWBZQ Product Title: Ecosox Bamboo Viscose Athletic Knee-High Cushion Tube Socks for Men & Women | Super Soft. Your Feet Dry & Blister-Free Rating: 4.9/5 Features: 80% Viscose from Bamboo, 10% Nylon, 5% Polyester, 3% Rubber, 2% Spandex Made in USA Machine Wash Made of Eco-Friendly Bamboo Viscose for Ultra-Soft Feel Moderate cushioning in ball/heel protects against blisters Helps Control and Prevent Foot Odor Thermo-Regulating to Help Regulate Skin Temperature Exclusive EcoSox construction wicks away moisture A smooth integrated toe seam reduces friction. Description: Missing Price: $10.00 Categories: Sports & Outdoors Clothing Boys Socks
    question: 
    socks

    Answer based on the Amazon datasets:
 if the user wants to buy this product, what should they do?
    Please only answer in English

assistant <think>
</think>Since I cannot browse live Amazon data in real-time to see current prices or availability, please check your local search bar or visit amazon.com directly to verify the price and stock status for the listed products before purchasing. However, here is how you can proceed based on the provided information:

If you want to buy Bauer Hockey Performance Skate Socks, purchase them online at $18.99. They are sold as pairs (“Sold as (1) Pair”) and come in sizes XS, S, M, L, and XL.
If you want to buy Swiftwick MAXUS ZERO Golf & Running Socks, purchase them online at $16.99. These have two different cuff options (Zero or Tab).
If you want to buy Ecosox Bamboo Viscose Athletic Knee-High Cushion Tube Socks, note that their price ($10.00) appears lower than the others but still requires checking current availability since “Missing” suggests no physical stock details were provided yet.
You may also consider these alternative brands mentioned in the context:

Smartwool Kids Wintersport Neo Native: Available for purchase online at $X.XXX.
Swiftkind (likely meant by Swiftwick): Available online at $X.XXX.
Smoothieco Bamboo/SuperSole: Available online at $X.XXX.
Polaris Comfort: Available online at $X.XXX.
Columbia Bigfoot Crew Fleece: Available online at $X.XXX.
Reebok Classic Runner Socks: Available online at $X.XXX.
Lululemon Underwear: Available online at $X.XXX.
Wicked Woodwork: Available online at $X.XXX.
Please double-check the latest prices and inventory via the official retailer’s website to ensure you find items ready for immediate delivery!
```

Overall the evaluation is quite on point and performs relatively well for such a small model. Although some queries are not fully completed, generally they are factually correct without obvious errors.  

Limitations include slow speed and not taking into too much tokens. This hybrid RAG model uses fixed weights between bm25 and semantic search, which could be a problem if one retriever is not very confident about certain queries. 

Dynamic weights can be applied according to their scores instead. We also suggest to improve performance with a larger LLM models.