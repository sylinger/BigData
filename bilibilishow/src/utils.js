// utils.js
export function addLine(sentence, interval = 6) {
  sentence = sentence.replace(/\s/g, '');
  const regex = new RegExp(`(.{${interval}})`, 'g');
  return sentence.replace(regex, '$1\n');
}
  
export function addLineEng(sentence) {
  return sentence.replace(/\s/g, '\n');
}

export function mapToList(data) {
  return data.map(item => [item.word, parseInt(item.count)]);
}
  