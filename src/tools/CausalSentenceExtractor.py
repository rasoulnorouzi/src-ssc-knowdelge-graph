class causalityExtractor:
    def __init__(
                self, model, tokenizer, threshold=0.9, batch_size=32
                ):
        
        self.model = model
        self.tokenizer = tokenizer
        self.threshold = threshold
        self.batch_size = batch_size


    def batch_generator(self, sentences):
        for i in range(0, len(sentences), self.batch_size):
            yield sentences[i:i+self.batch_size]


    def forward(self, sentences):
        causal_sentence = []
        for batch in self.batch_generator(sentences):
            inputs = self.tokenizer(batch, return_tensors='pt', padding=True, truncation=True)
            outputs = self.model(**inputs)
            predicted_labels = [1 if outputs.logits[i][1] > self.threshold else 0 for i in range(len(outputs.logits))]
            
            for i, label in enumerate(predicted_labels):
                if label == 1:
                    causal_sentence.append(batch[i])
        return causal_sentence