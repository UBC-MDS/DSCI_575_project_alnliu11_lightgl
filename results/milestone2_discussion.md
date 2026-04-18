# Milestone 2 Discussion
## 1.2 Describe LLM Model Choice
We decide to use `qwen3.5:2b` because it generates text on my laptop at a reasonable speed, and its response looks reasonably good.

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
- Accuracy: yes, it does find some some camping tent that are waterproof.
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
- Accuracy: no, it does not generate any response
- Completeness: No response.
- Fluency: No response.
```
Response:

```
Overall the evaluation is quite on point and performs relatively well for such a small model.
2 limitation includes slow speed and cannot take into too much tokens.
Suggest to improve performance with a larger LLM models.